"""Spark v1 async Python client — connects to the broker Unix socket.

Authority: docs/design/spark-api.md

Usage::

    async with SparkClient(slug="my-plugin", sock_path=Path("var/hearth/run/spark.sock"),
                           permissions=my_perm) as client:
        result = await client.call("other-plugin", "method", {"arg": 1})
        await client.publish("events.created", {"id": 42})
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any

from spark.protocol import new_id, read_frame, write_frame

DEFAULT_TIMEOUT_MS = 5000


class SparkError(Exception):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


class SparkClient:
    def __init__(
        self,
        slug: str,
        sock_path: Path = Path("var/hearth/run/spark.sock"),
        timeout_ms: int = DEFAULT_TIMEOUT_MS,
    ) -> None:
        self._slug = slug
        self._sock_path = sock_path
        self._timeout_ms = timeout_ms
        self._reader: asyncio.StreamReader | None = None
        self._writer: asyncio.StreamWriter | None = None
        self._pending: dict[str, asyncio.Future[dict[str, Any]]] = {}
        self._listener_task: asyncio.Task[None] | None = None
        self._event_handlers: dict[str, list[Any]] = {}

    async def connect(self) -> None:
        self._reader, self._writer = await asyncio.open_unix_connection(str(self._sock_path))
        await write_frame(self._writer, {"v": 1, "kind": "register", "from": self._slug})
        # wait for the broker's "registered" ack before returning so callers know
        # this plugin is visible to other plugins
        ack = await read_frame(self._reader)
        if ack.get("kind") != "registered":
            raise SparkError("PROTOCOL", f"expected registered ack, got {ack.get('kind')}")
        self._listener_task = asyncio.create_task(self._listen())

    async def close(self) -> None:
        if self._listener_task:
            self._listener_task.cancel()
            try:
                await self._listener_task
            except asyncio.CancelledError:
                pass
        if self._writer:
            self._writer.close()
            try:
                await self._writer.wait_closed()
            except Exception:
                pass

    async def __aenter__(self) -> SparkClient:
        await self.connect()
        return self

    async def __aexit__(self, *_: Any) -> None:
        await self.close()

    async def call(
        self,
        target: str,
        method: str,
        params: dict[str, Any] | None = None,
        timeout_ms: int | None = None,
    ) -> dict[str, Any]:
        req_id = new_id()
        timeout = (timeout_ms if timeout_ms is not None else self._timeout_ms) / 1000
        fut: asyncio.Future[dict[str, Any]] = asyncio.get_event_loop().create_future()
        self._pending[req_id] = fut
        frame: dict[str, Any] = {
            "v": 1,
            "id": req_id,
            "kind": "call",
            "from": self._slug,
            "to": target,
            "method": method,
        }
        if params:
            frame["params"] = params
        await write_frame(self._writer, frame)  # type: ignore[arg-type]
        try:
            reply = await asyncio.wait_for(fut, timeout=timeout)
        except TimeoutError:
            self._pending.pop(req_id, None)
            raise SparkError("TIMEOUT", f"no reply from {target}.{method} within {timeout_ms}ms")
        if reply.get("kind") == "error":
            raise SparkError(reply.get("code", "UNKNOWN"), reply.get("message", ""))
        return reply.get("result", reply)

    async def publish(self, topic: str, payload: dict[str, Any] | None = None) -> None:
        frame: dict[str, Any] = {
            "v": 1,
            "id": new_id(),
            "kind": "publish",
            "from": self._slug,
            "topic": topic,
        }
        if payload:
            frame["payload"] = payload
        await write_frame(self._writer, frame)  # type: ignore[arg-type]

    async def subscribe(self, topic_pattern: str, handler: Any) -> None:
        self._event_handlers.setdefault(topic_pattern, []).append(handler)
        await write_frame(
            self._writer,
            {  # type: ignore[arg-type]
                "v": 1,
                "id": new_id(),
                "kind": "subscribe",
                "from": self._slug,
                "topic_pattern": topic_pattern,
            },
        )

    async def _listen(self) -> None:
        assert self._reader is not None
        try:
            while True:
                frame = await read_frame(self._reader)
                kind = frame.get("kind")
                req_id = frame.get("id", "")
                if kind in ("reply", "error"):
                    fut = self._pending.pop(req_id, None)
                    if fut is not None and not fut.done():
                        fut.set_result(frame)
                elif kind == "event":
                    await self._dispatch_event(frame)
        except (asyncio.IncompleteReadError, ConnectionResetError, asyncio.CancelledError):
            pass

    async def _dispatch_event(self, frame: dict[str, Any]) -> None:
        topic = frame.get("topic", "")
        for pattern, handlers in self._event_handlers.items():
            from spark.permissions import topic_matches_pattern

            if topic_matches_pattern(topic, pattern):
                for handler in handlers:
                    if asyncio.iscoroutinefunction(handler):
                        await handler(frame)
                    else:
                        handler(frame)

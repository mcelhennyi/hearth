"""Spark v1 broker — Unix-socket message broker for inter-plugin calls.

Authority: docs/design/spark-api.md

Wire format: 4-byte big-endian length prefix + UTF-8 JSON.
Each plugin connects and identifies itself with a {kind: "register"} frame.
The broker routes call/reply, fans out publish→event, and enforces permissions.
All frames are appended to the audit log at var/hearth/log/spark.jsonl.

Design note: The broker runs as a single asyncio task; all state is in-process.
Phase 2 will add cross-host transport (Ember) without changing the client API.
"""

from __future__ import annotations

import asyncio
import inspect
import json
import logging
import os
import time
from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import Any

from spark.permissions import (
    PluginPermissions,
    can_call,
    can_publish,
    can_subscribe,
    topic_matches_pattern,
)
from spark.protocol import make_error, new_id, read_frame, write_frame

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT_MS = 5000

SparkMethodHandler = Callable[[dict[str, Any]], dict[str, Any] | Awaitable[dict[str, Any]]]


class _Connection:
    def __init__(self, slug: str, writer: asyncio.StreamWriter) -> None:
        self.slug = slug
        self.writer = writer
        # topic patterns this plugin is subscribed to
        self.subscriptions: set[str] = set()


class SparkBroker:
    """In-process Spark v1 broker.

    Usage::

        broker = SparkBroker(sock_path=Path("var/hearth/run/spark.sock"),
                             log_path=Path("var/hearth/log/spark.jsonl"))
        await broker.serve_forever()
    """

    def __init__(
        self,
        sock_path: Path = Path("var/hearth/run/spark.sock"),
        log_path: Path = Path("var/hearth/log/spark.jsonl"),
        permissions: dict[str, PluginPermissions] | None = None,
    ) -> None:
        self._sock_path = sock_path
        self._log_path = log_path
        # slug → PluginPermissions (populated from Tinder manifests on register)
        self._permissions: dict[str, PluginPermissions] = permissions or {}
        # slug → _Connection
        self._connections: dict[str, _Connection] = {}
        # request id → asyncio.Future for pending calls
        self._pending: dict[str, asyncio.Future[dict[str, Any]]] = {}
        # (slug, method) → in-process handler for hub-owned/built-in Spark surfaces
        self._local_methods: dict[tuple[str, str], SparkMethodHandler] = {}
        self._server: asyncio.AbstractServer | None = None
        self._log_fh: Any = None

    def register_plugin(self, slug: str, perm: PluginPermissions) -> None:
        """Pre-register a plugin's permissions (called before it connects)."""
        self._permissions[slug] = perm

    def register_method(self, slug: str, method: str, handler: SparkMethodHandler) -> None:
        """Register an in-process Spark method handler.

        Built-in platform capabilities can live in the hub process before they
        have a long-running plugin socket client. Broker permission checks still
        apply before the handler is invoked.
        """
        self._local_methods[(slug, method)] = handler

    async def serve_forever(self) -> None:
        sock = str(self._sock_path)
        self._sock_path.parent.mkdir(parents=True, exist_ok=True)
        if os.path.exists(sock):
            os.unlink(sock)
        self._log_path.parent.mkdir(parents=True, exist_ok=True)
        self._log_fh = open(self._log_path, "a", encoding="utf-8")  # noqa: SIM115
        self._server = await asyncio.start_unix_server(self._handle_client, path=sock)
        os.chmod(sock, 0o660)
        async with self._server:
            await self._server.serve_forever()

    async def stop(self) -> None:
        if self._server:
            self._server.close()
            await self._server.wait_closed()
        if self._log_fh:
            self._log_fh.close()

    async def _handle_client(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        conn: _Connection | None = None
        try:
            # First frame must be a register
            reg = await asyncio.wait_for(read_frame(reader), timeout=10)
            if reg.get("kind") != "register" or "from" not in reg:
                writer.close()
                return
            slug = reg["from"]
            perm = self._permissions.get(slug, PluginPermissions())
            conn = _Connection(slug=slug, writer=writer)
            self._connections[slug] = conn
            logger.debug("Spark: %s connected", slug)
            await write_frame(writer, {"v": 1, "kind": "registered", "from": slug})

            while True:
                try:
                    frame = await read_frame(reader)
                except (asyncio.IncompleteReadError, ConnectionResetError):
                    break
                await self._dispatch(frame, conn, perm)
        finally:
            if conn is not None:
                self._connections.pop(conn.slug, None)
                # Cancel any pending calls from this plugin
                for fut in list(self._pending.values()):
                    if not fut.done():
                        fut.cancel()
            writer.close()

    async def _dispatch(
        self, frame: dict[str, Any], conn: _Connection, perm: PluginPermissions
    ) -> None:
        kind = frame.get("kind")
        req_id = frame.get("id", new_id())
        t0 = time.time()

        if kind == "call":
            await self._handle_call(frame, conn, perm, req_id, t0)
        elif kind == "reply":
            await self._handle_reply(frame, req_id, t0)
        elif kind == "publish":
            await self._handle_publish(frame, conn, perm, req_id, t0)
        elif kind == "subscribe":
            await self._handle_subscribe(frame, conn, perm, req_id)
        elif kind == "unsubscribe":
            pattern = frame.get("topic_pattern", "")
            conn.subscriptions.discard(pattern)
            await write_frame(conn.writer, {"v": 1, "id": req_id, "kind": "ack"})
        else:
            await write_frame(conn.writer, make_error(req_id, "INTERNAL", f"unknown kind: {kind}"))

    async def _handle_call(
        self,
        frame: dict[str, Any],
        conn: _Connection,
        perm: PluginPermissions,
        req_id: str,
        t0: float,
    ) -> None:
        target_slug = frame.get("to", "")
        method = frame.get("method", "")
        timeout_ms = frame.get("timeout_ms", DEFAULT_TIMEOUT_MS)
        local_handler = self._local_methods.get((target_slug, method))

        if local_handler is not None:
            await self._handle_local_call(frame, conn, perm, req_id, t0, local_handler)
            return

        if target_slug not in self._connections:
            err = make_error(req_id, "UNKNOWN_PLUGIN", f"plugin '{target_slug}' not connected")
            await write_frame(conn.writer, err)
            self._audit(frame, ok=False, latency_ms=(time.time() - t0) * 1000)
            return

        if not can_call(perm, target_slug, method):
            msg = f"not allowed to call {target_slug}.{method}"
            err = make_error(req_id, "PERMISSION_DENIED", msg)
            await write_frame(conn.writer, err)
            self._audit(frame, ok=False, latency_ms=(time.time() - t0) * 1000)
            return

        target_conn = self._connections[target_slug]
        fut: asyncio.Future[dict[str, Any]] = asyncio.get_event_loop().create_future()
        self._pending[req_id] = fut

        fwd = {**frame, "ts": time.time()}
        await write_frame(target_conn.writer, fwd)

        try:
            reply = await asyncio.wait_for(fut, timeout=timeout_ms / 1000)
            await write_frame(conn.writer, reply)
            self._audit(frame, ok=True, latency_ms=(time.time() - t0) * 1000)
        except TimeoutError:
            self._pending.pop(req_id, None)
            tmsg = f"no reply from {target_slug} within {timeout_ms}ms"
            err = make_error(req_id, "TIMEOUT", tmsg)
            await write_frame(conn.writer, err)
            self._audit(frame, ok=False, latency_ms=(time.time() - t0) * 1000)

    async def _handle_local_call(
        self,
        frame: dict[str, Any],
        conn: _Connection,
        perm: PluginPermissions,
        req_id: str,
        t0: float,
        handler: SparkMethodHandler,
    ) -> None:
        target_slug = frame.get("to", "")
        method = frame.get("method", "")

        if not can_call(perm, target_slug, method):
            msg = f"not allowed to call {target_slug}.{method}"
            err = make_error(req_id, "PERMISSION_DENIED", msg)
            await write_frame(conn.writer, err)
            self._audit(
                frame,
                ok=False,
                latency_ms=(time.time() - t0) * 1000,
                local_handler=True,
            )
            return

        params = frame.get("params", frame.get("body", {}))
        if not isinstance(params, dict):
            err = make_error(req_id, "INVALID_BODY", "Spark method params must be an object.")
            await write_frame(conn.writer, err)
            self._audit(
                frame,
                ok=False,
                latency_ms=(time.time() - t0) * 1000,
                local_handler=True,
            )
            return

        try:
            result = handler(params)
            if inspect.isawaitable(result):
                result = await result
            await write_frame(conn.writer, {"v": 1, "id": req_id, "kind": "reply", "result": result})
            self._audit(
                frame,
                ok=True,
                latency_ms=(time.time() - t0) * 1000,
                local_handler=True,
            )
        except Exception:
            logger.exception("Spark local method failed: %s.%s", target_slug, method)
            err = make_error(req_id, "INTERNAL", f"local method failed: {target_slug}.{method}")
            await write_frame(conn.writer, err)
            self._audit(
                frame,
                ok=False,
                latency_ms=(time.time() - t0) * 1000,
                local_handler=True,
            )

    async def _handle_reply(self, frame: dict[str, Any], req_id: str, t0: float) -> None:
        fut = self._pending.pop(req_id, None)
        if fut is not None and not fut.done():
            fut.set_result(frame)

    async def _handle_publish(
        self,
        frame: dict[str, Any],
        conn: _Connection,
        perm: PluginPermissions,
        req_id: str,
        t0: float,
    ) -> None:
        topic = frame.get("topic", "")

        if not can_publish(perm, topic):
            err = make_error(req_id, "PERMISSION_DENIED", f"not allowed to publish {topic}")
            await write_frame(conn.writer, err)
            self._audit(frame, ok=False, latency_ms=(time.time() - t0) * 1000)
            return

        event = {**frame, "kind": "event", "ts": time.time()}
        fan_count = 0
        for sub_conn in list(self._connections.values()):
            if sub_conn.slug == conn.slug:
                continue
            for pattern in sub_conn.subscriptions:
                if topic_matches_pattern(topic, pattern):
                    await write_frame(sub_conn.writer, event)
                    fan_count += 1
                    break

        await write_frame(conn.writer, {"v": 1, "id": req_id, "kind": "ack"})
        self._audit(frame, ok=True, latency_ms=(time.time() - t0) * 1000, fan_count=fan_count)

    async def _handle_subscribe(
        self,
        frame: dict[str, Any],
        conn: _Connection,
        perm: PluginPermissions,
        req_id: str,
    ) -> None:
        pattern = frame.get("topic_pattern", "")
        if not can_subscribe(perm, pattern):
            err = make_error(req_id, "PERMISSION_DENIED", f"not allowed to subscribe to {pattern}")
            await write_frame(conn.writer, err)
            return
        conn.subscriptions.add(pattern)
        await write_frame(conn.writer, {"v": 1, "id": req_id, "kind": "ack"})

    def _audit(self, frame: dict[str, Any], *, ok: bool, latency_ms: float, **extra: Any) -> None:
        if self._log_fh is None:
            return
        record = {
            "ts": time.time(),
            "id": frame.get("id", ""),
            "from": frame.get("from", ""),
            "to": frame.get("to", ""),
            "kind": frame.get("kind", ""),
            "method": frame.get("method"),
            "topic": frame.get("topic"),
            "ok": ok,
            "latency_ms": round(latency_ms, 3),
        }
        record.update(extra)
        self._log_fh.write(json.dumps(record) + "\n")
        self._log_fh.flush()

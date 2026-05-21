"""Spark v1 wire protocol helpers — frame encoding and envelope models.

Authority: docs/design/spark-api.md
"""

from __future__ import annotations

import json
import struct
import time
import uuid
from typing import Any, Literal

SparkKind = Literal[
    "call", "reply", "error", "publish", "subscribe", "unsubscribe", "event", "ack", "register"
]

_HEADER = struct.Struct(">I")  # 4-byte big-endian unsigned int


def encode_frame(envelope: dict[str, Any]) -> bytes:
    payload = json.dumps(envelope).encode("utf-8")
    return _HEADER.pack(len(payload)) + payload


def decode_frame(data: bytes) -> dict[str, Any]:
    if len(data) < 4:
        raise ValueError("frame too short")
    (length,) = _HEADER.unpack_from(data, 0)
    if len(data) != 4 + length:
        raise ValueError(f"frame length mismatch: header={length} actual={len(data) - 4}")
    return json.loads(data[4:].decode("utf-8"))


async def read_frame(reader: Any) -> dict[str, Any]:
    header = await reader.readexactly(4)
    (length,) = _HEADER.unpack_from(header, 0)
    payload = await reader.readexactly(length)
    return json.loads(payload.decode("utf-8"))


async def write_frame(writer: Any, envelope: dict[str, Any]) -> None:
    writer.write(encode_frame(envelope))
    await writer.drain()


def new_id() -> str:
    return str(uuid.uuid4())


def make_error(req_id: str, code: str, message: str) -> dict[str, Any]:
    return {
        "v": 1,
        "id": req_id,
        "kind": "error",
        "code": code,
        "message": message,
        "ts": time.time(),
    }

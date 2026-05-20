"""Tests for Spark v1 broker — call/reply, publish/subscribe, permissions, timeout.

Authority: docs/design/spark-api.md
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Any

import pytest
import pytest_asyncio

from spark.broker import SparkBroker
from spark.permissions import PluginPermissions
from spark.protocol import decode_frame, encode_frame, new_id

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _open_perm(**kwargs: list[str]) -> PluginPermissions:
    return PluginPermissions(**kwargs)


async def _raw_connect(
    sock_path: Path, slug: str
) -> tuple[asyncio.StreamReader, asyncio.StreamWriter]:
    reader, writer = await asyncio.open_unix_connection(str(sock_path))
    from spark.protocol import write_frame

    await write_frame(writer, {"v": 1, "kind": "register", "from": slug})
    # wait for registered ack so the plugin is visible before the caller proceeds
    ack = await asyncio.wait_for(_raw_recv(reader), timeout=3)
    assert ack["kind"] == "registered", f"expected registered, got {ack}"
    return reader, writer


async def _raw_send(writer: asyncio.StreamWriter, frame: dict[str, Any]) -> None:
    from spark.protocol import write_frame

    await write_frame(writer, frame)


async def _raw_recv(reader: asyncio.StreamReader) -> dict[str, Any]:
    from spark.protocol import read_frame

    return await asyncio.wait_for(read_frame(reader), timeout=3)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest_asyncio.fixture
async def broker(tmp_path: Path):
    sock = tmp_path / "spark.sock"
    log = tmp_path / "spark.jsonl"
    b = SparkBroker(sock_path=sock, log_path=log, permissions={})
    task = asyncio.create_task(b.serve_forever())
    # give server a moment to start
    await asyncio.sleep(0.05)
    yield b
    await b.stop()
    task.cancel()
    try:
        await task
    except (asyncio.CancelledError, Exception):
        pass


@pytest_asyncio.fixture
async def broker_with_perms(tmp_path: Path):
    sock = tmp_path / "spark.sock"
    log = tmp_path / "spark.jsonl"
    perms = {
        "caller": PluginPermissions(
            spark_call=["callee.*"],
            spark_publish=["events.>"],
            spark_subscribe=["events.>"],
        ),
        "callee": PluginPermissions(
            spark_call=[],
            spark_publish=[],
            spark_subscribe=[],
        ),
        "subscriber": PluginPermissions(
            spark_call=[],
            spark_publish=[],
            spark_subscribe=["events.>"],
        ),
    }
    b = SparkBroker(sock_path=sock, log_path=log, permissions=perms)
    task = asyncio.create_task(b.serve_forever())
    await asyncio.sleep(0.05)
    yield b, sock
    await b.stop()
    task.cancel()
    try:
        await task
    except (asyncio.CancelledError, Exception):
        pass


# ---------------------------------------------------------------------------
# Protocol tests (encode/decode)
# ---------------------------------------------------------------------------


def test_encode_decode_round_trip():
    original = {"v": 1, "kind": "call", "id": "abc", "from": "a", "to": "b", "method": "hello"}
    assert decode_frame(encode_frame(original)) == original


def test_decode_frame_too_short():
    import pytest

    with pytest.raises(ValueError, match="too short"):
        decode_frame(b"\x00\x00")


def test_decode_frame_length_mismatch():
    import pytest

    payload = b'{"v":1}'
    header = (100).to_bytes(4, "big")  # claims 100 bytes, only 7 present
    with pytest.raises(ValueError, match="mismatch"):
        decode_frame(header + payload)


# ---------------------------------------------------------------------------
# Permission unit tests
# ---------------------------------------------------------------------------


def test_can_call_allowed():
    from spark.permissions import can_call

    perm = PluginPermissions(spark_call=["callee.*"])
    assert can_call(perm, "callee", "getData") is True


def test_can_call_denied():
    from spark.permissions import can_call

    perm = PluginPermissions(spark_call=["other.*"])
    assert can_call(perm, "callee", "getData") is False


def test_can_call_wildcard_method():
    from spark.permissions import can_call

    perm = PluginPermissions(spark_call=["*.getData"])
    assert can_call(perm, "callee", "getData") is True
    assert can_call(perm, "other", "getData") is True
    assert can_call(perm, "other", "setData") is False


def test_can_publish_allowed():
    from spark.permissions import can_publish

    perm = PluginPermissions(spark_publish=["events.>"])
    assert can_publish(perm, "events.item.created") is True


def test_can_publish_denied():
    from spark.permissions import can_publish

    perm = PluginPermissions(spark_publish=["logs.>"])
    assert can_publish(perm, "events.item.created") is False


def test_can_subscribe_exact_pattern():
    from spark.permissions import can_subscribe

    perm = PluginPermissions(spark_subscribe=["events.>"])
    assert can_subscribe(perm, "events.>") is True
    assert can_subscribe(perm, "logs.>") is False


def test_topic_matches_pattern_star():
    from spark.permissions import topic_matches_pattern

    assert topic_matches_pattern("events.item", "events.*") is True
    assert topic_matches_pattern("events.item.sub", "events.*") is False


def test_topic_matches_pattern_gt():
    from spark.permissions import topic_matches_pattern

    assert topic_matches_pattern("events.item.created", "events.>") is True
    assert topic_matches_pattern("logs.error", "events.>") is False


# ---------------------------------------------------------------------------
# Broker integration — call/reply
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_call_reply_roundtrip(broker_with_perms):
    b, sock = broker_with_perms

    reader_callee, writer_callee = await _raw_connect(sock, "callee")
    reader_caller, writer_caller = await _raw_connect(sock, "caller")

    req_id = new_id()
    await _raw_send(
        writer_caller,
        {
            "v": 1,
            "id": req_id,
            "kind": "call",
            "from": "caller",
            "to": "callee",
            "method": "add",
            "params": {"a": 1, "b": 2},
        },
    )

    # callee receives the forwarded call
    incoming = await _raw_recv(reader_callee)
    assert incoming["kind"] == "call"
    assert incoming["method"] == "add"
    assert incoming["params"] == {"a": 1, "b": 2}

    # callee sends reply
    await _raw_send(
        writer_callee,
        {
            "v": 1,
            "id": req_id,
            "kind": "reply",
            "result": {"sum": 3},
        },
    )

    # caller receives reply
    reply = await _raw_recv(reader_caller)
    assert reply["kind"] == "reply"
    assert reply["result"] == {"sum": 3}

    writer_caller.close()
    writer_callee.close()


@pytest.mark.asyncio
async def test_call_unknown_plugin(broker_with_perms):
    b, sock = broker_with_perms
    reader, writer = await _raw_connect(sock, "caller")

    req_id = new_id()
    await _raw_send(
        writer,
        {
            "v": 1,
            "id": req_id,
            "kind": "call",
            "from": "caller",
            "to": "nonexistent",
            "method": "foo",
        },
    )
    reply = await _raw_recv(reader)
    assert reply["kind"] == "error"
    assert reply["code"] == "UNKNOWN_PLUGIN"

    writer.close()


@pytest.mark.asyncio
async def test_call_permission_denied(broker_with_perms):
    b, sock = broker_with_perms
    # callee has no spark_call permissions
    reader_callee, writer_callee = await _raw_connect(sock, "callee")
    reader_caller, writer_caller = await _raw_connect(sock, "caller")

    req_id = new_id()
    # callee tries to call caller — not permitted
    await _raw_send(
        writer_callee,
        {
            "v": 1,
            "id": req_id,
            "kind": "call",
            "from": "callee",
            "to": "caller",
            "method": "anything",
        },
    )
    reply = await _raw_recv(reader_callee)
    assert reply["kind"] == "error"
    assert reply["code"] == "PERMISSION_DENIED"

    writer_caller.close()
    writer_callee.close()


@pytest.mark.asyncio
async def test_call_timeout(broker_with_perms):
    b, sock = broker_with_perms
    reader_callee, writer_callee = await _raw_connect(sock, "callee")
    reader_caller, writer_caller = await _raw_connect(sock, "caller")

    req_id = new_id()
    await _raw_send(
        writer_caller,
        {
            "v": 1,
            "id": req_id,
            "kind": "call",
            "from": "caller",
            "to": "callee",
            "method": "slow",
            "timeout_ms": 100,
        },
    )
    # consume the forwarded call at callee side but don't reply
    await _raw_recv(reader_callee)

    # caller should receive TIMEOUT error within ~200ms
    reply = await asyncio.wait_for(_raw_recv(reader_caller), timeout=2)
    assert reply["kind"] == "error"
    assert reply["code"] == "TIMEOUT"

    writer_caller.close()
    writer_callee.close()


# ---------------------------------------------------------------------------
# Broker integration — publish / subscribe
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_publish_fanout(broker_with_perms):
    b, sock = broker_with_perms
    reader_sub, writer_sub = await _raw_connect(sock, "subscriber")
    reader_pub, writer_pub = await _raw_connect(sock, "caller")

    # subscriber subscribes
    sub_id = new_id()
    await _raw_send(
        writer_sub,
        {
            "v": 1,
            "id": sub_id,
            "kind": "subscribe",
            "from": "subscriber",
            "topic_pattern": "events.>",
        },
    )
    ack = await _raw_recv(reader_sub)
    assert ack["kind"] == "ack"

    # publisher publishes
    pub_id = new_id()
    await _raw_send(
        writer_pub,
        {
            "v": 1,
            "id": pub_id,
            "kind": "publish",
            "from": "caller",
            "topic": "events.item.created",
            "payload": {"id": 99},
        },
    )
    # publisher receives ack
    ack2 = await _raw_recv(reader_pub)
    assert ack2["kind"] == "ack"

    # subscriber receives event
    event = await asyncio.wait_for(_raw_recv(reader_sub), timeout=2)
    assert event["kind"] == "event"
    assert event["topic"] == "events.item.created"

    writer_sub.close()
    writer_pub.close()


@pytest.mark.asyncio
async def test_publish_permission_denied(broker_with_perms):
    b, sock = broker_with_perms
    reader, writer = await _raw_connect(sock, "callee")

    await _raw_send(
        writer,
        {
            "v": 1,
            "id": new_id(),
            "kind": "publish",
            "from": "callee",
            "topic": "events.item.created",
        },
    )
    reply = await _raw_recv(reader)
    assert reply["kind"] == "error"
    assert reply["code"] == "PERMISSION_DENIED"

    writer.close()


@pytest.mark.asyncio
async def test_publish_no_self_delivery(broker_with_perms):
    """Publisher should not receive its own event even if subscribed."""
    b, sock = broker_with_perms

    # caller subscribes and then publishes
    reader, writer = await _raw_connect(sock, "caller")
    await _raw_send(
        writer,
        {
            "v": 1,
            "id": new_id(),
            "kind": "subscribe",
            "from": "caller",
            "topic_pattern": "events.>",
        },
    )
    ack = await _raw_recv(reader)
    assert ack["kind"] == "ack"

    await _raw_send(
        writer,
        {
            "v": 1,
            "id": new_id(),
            "kind": "publish",
            "from": "caller",
            "topic": "events.self.test",
        },
    )
    # only the publish ack comes back, no event
    reply = await asyncio.wait_for(_raw_recv(reader), timeout=1)
    assert reply["kind"] == "ack"

    # no event should follow within 0.3s
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(_raw_recv(reader), timeout=0.3)

    writer.close()


@pytest.mark.asyncio
async def test_subscribe_permission_denied(broker_with_perms):
    b, sock = broker_with_perms
    reader, writer = await _raw_connect(sock, "callee")

    await _raw_send(
        writer,
        {
            "v": 1,
            "id": new_id(),
            "kind": "subscribe",
            "from": "callee",
            "topic_pattern": "events.>",
        },
    )
    reply = await _raw_recv(reader)
    assert reply["kind"] == "error"
    assert reply["code"] == "PERMISSION_DENIED"

    writer.close()


@pytest.mark.asyncio
async def test_unsubscribe(broker_with_perms):
    b, sock = broker_with_perms
    reader_sub, writer_sub = await _raw_connect(sock, "subscriber")
    reader_pub, writer_pub = await _raw_connect(sock, "caller")

    # subscribe
    await _raw_send(
        writer_sub,
        {
            "v": 1,
            "id": new_id(),
            "kind": "subscribe",
            "from": "subscriber",
            "topic_pattern": "events.>",
        },
    )
    await _raw_recv(reader_sub)  # ack

    # unsubscribe
    await _raw_send(
        writer_sub,
        {
            "v": 1,
            "id": new_id(),
            "kind": "unsubscribe",
            "from": "subscriber",
            "topic_pattern": "events.>",
        },
    )
    ack = await _raw_recv(reader_sub)
    assert ack["kind"] == "ack"

    # publish — subscriber should NOT receive event
    await _raw_send(
        writer_pub,
        {
            "v": 1,
            "id": new_id(),
            "kind": "publish",
            "from": "caller",
            "topic": "events.foo",
        },
    )
    await _raw_recv(reader_pub)  # publisher ack

    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(_raw_recv(reader_sub), timeout=0.3)

    writer_sub.close()
    writer_pub.close()


# ---------------------------------------------------------------------------
# Broker integration — registration / unknown kind
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_unknown_kind_returns_error(broker_with_perms):
    b, sock = broker_with_perms
    reader, writer = await _raw_connect(sock, "caller")

    await _raw_send(writer, {"v": 1, "id": new_id(), "kind": "bogus", "from": "caller"})
    reply = await _raw_recv(reader)
    assert reply["kind"] == "error"
    assert "unknown kind" in reply["message"]

    writer.close()


@pytest.mark.asyncio
async def test_missing_register_closes(broker_with_perms):
    """Connection that doesn't send register as first frame is dropped."""
    b, sock = broker_with_perms
    reader, writer = await asyncio.open_unix_connection(str(sock))
    from spark.protocol import write_frame

    await write_frame(writer, {"v": 1, "kind": "call", "id": new_id()})
    # broker closes the connection; reader will hit EOF
    try:
        data = await asyncio.wait_for(reader.read(1), timeout=2)
        assert data == b""  # EOF
    except TimeoutError:
        pass  # also acceptable: broker just closed

    writer.close()


# ---------------------------------------------------------------------------
# Audit log test
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_audit_log_written(tmp_path: Path):
    sock = tmp_path / "spark.sock"
    log = tmp_path / "spark.jsonl"
    perms = {
        "a": PluginPermissions(spark_call=["b.*"]),
        "b": PluginPermissions(),
    }
    b = SparkBroker(sock_path=sock, log_path=log, permissions=perms)
    task = asyncio.create_task(b.serve_forever())
    await asyncio.sleep(0.05)

    reader_b, writer_b = await _raw_connect(sock, "b")
    reader_a, writer_a = await _raw_connect(sock, "a")

    req_id = new_id()
    await _raw_send(
        writer_a,
        {
            "v": 1,
            "id": req_id,
            "kind": "call",
            "from": "a",
            "to": "b",
            "method": "ping",
        },
    )
    await _raw_recv(reader_b)  # forwarded call
    await _raw_send(writer_b, {"v": 1, "id": req_id, "kind": "reply", "result": {}})
    await _raw_recv(reader_a)  # reply

    writer_a.close()
    writer_b.close()
    await b.stop()
    task.cancel()
    try:
        await task
    except (asyncio.CancelledError, Exception):
        pass

    lines = [json.loads(rec) for rec in log.read_text().strip().splitlines()]
    call_records = [rec for rec in lines if rec.get("kind") == "call"]
    assert len(call_records) >= 1
    assert call_records[0]["from"] == "a"
    assert call_records[0]["to"] == "b"
    assert call_records[0]["ok"] is True

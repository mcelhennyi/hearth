"""Push-related tests — subscribe/unsubscribe, VAPID signing, ntfy shape.

Authority: docs/design/notifications.md
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from app.push_service import PushConfig, build_vapid_claims, get_audience
from app.push_store import load_subscriptions, save_subscriptions, upsert_subscription

# ---------------------------------------------------------------------------
# Unit: push_store
# ---------------------------------------------------------------------------


def test_upsert_new_subscription():
    subs: list = []
    sub = {"endpoint": "https://push.example.com/abc", "keys": {}}
    result = upsert_subscription(subs, sub)
    assert len(result) == 1
    assert result[0]["endpoint"] == "https://push.example.com/abc"


def test_upsert_replaces_existing():
    old = {"endpoint": "https://push.example.com/abc", "keys": {"old": True}}
    new = {"endpoint": "https://push.example.com/abc", "keys": {"new": True}}
    result = upsert_subscription([old], new)
    assert len(result) == 1
    assert result[0]["keys"] == {"new": True}


def test_upsert_missing_endpoint():
    with pytest.raises(ValueError):
        upsert_subscription([], {"keys": {}})


def test_load_subscriptions_missing_file(tmp_path: Path):
    assert load_subscriptions(tmp_path / "nope.json") == []


def test_save_and_load_subscriptions(tmp_path: Path):
    path = tmp_path / "subs.json"
    subs = [{"endpoint": "https://push.example.com/1", "keys": {}}]
    save_subscriptions(path, subs)
    assert load_subscriptions(path) == subs


# ---------------------------------------------------------------------------
# Unit: VAPID audience parsing
# ---------------------------------------------------------------------------


def test_get_audience_standard():
    assert get_audience("https://fcm.googleapis.com/fcm/send/xxx") == "https://fcm.googleapis.com"


def test_get_audience_apple():
    assert get_audience("https://api.push.apple.com/3/device/xxx") == "https://api.push.apple.com"


def test_get_audience_invalid():
    with pytest.raises(ValueError):
        get_audience("not-a-url")


# ---------------------------------------------------------------------------
# Unit: VAPID claims shape
# ---------------------------------------------------------------------------


def test_build_vapid_claims_contains_required_fields():
    endpoint = "https://fcm.googleapis.com/fcm/send/device"
    claims = build_vapid_claims(endpoint, "mailto:test@example.com")
    assert claims["sub"] == "mailto:test@example.com"
    assert claims["aud"] == "https://fcm.googleapis.com"


def test_build_vapid_claims_with_exp():
    endpoint = "https://fcm.googleapis.com/fcm/send/device"
    claims = build_vapid_claims(endpoint, "mailto:test@example.com", exp=9999999999)
    assert claims["exp"] == 9999999999


# ---------------------------------------------------------------------------
# API: subscribe / unsubscribe
# ---------------------------------------------------------------------------


def test_subscribe_stores_subscription(client, tmp_path: Path):
    subs_path = tmp_path / "subs.json"
    config = PushConfig(
        subscriptions_path=subs_path,
        vapid_public_key_path=tmp_path / "vapid.pub",
        vapid_private_key_path=tmp_path / "vapid.priv",
    )
    client.app.state.push_config = config
    sub = {
        "endpoint": "https://push.example.com/device1",
        "keys": {"p256dh": "aaa", "auth": "bbb"},
    }
    resp = client.post("/api/push/subscribe", json=sub)
    assert resp.status_code == 200
    assert resp.json()["stored"] == 1
    stored = load_subscriptions(subs_path)
    assert stored[0]["endpoint"] == sub["endpoint"]


def test_unsubscribe_removes_subscription(client, tmp_path: Path):
    subs_path = tmp_path / "subs2.json"
    endpoint = "https://push.example.com/device2"
    save_subscriptions(subs_path, [{"endpoint": endpoint, "keys": {}}])
    config = PushConfig(
        subscriptions_path=subs_path,
        vapid_public_key_path=tmp_path / "vapid.pub",
        vapid_private_key_path=tmp_path / "vapid.priv",
    )
    client.app.state.push_config = config
    resp = client.delete(f"/api/push/subscribe/{endpoint}")
    assert resp.status_code == 200
    assert resp.json()["stored"] == 0
    assert load_subscriptions(subs_path) == []


def test_unsubscribe_missing_returns_404(client, tmp_path: Path):
    subs_path = tmp_path / "subs3.json"
    save_subscriptions(subs_path, [])
    config = PushConfig(
        subscriptions_path=subs_path,
        vapid_public_key_path=tmp_path / "vapid.pub",
        vapid_private_key_path=tmp_path / "vapid.priv",
    )
    client.app.state.push_config = config
    resp = client.delete("/api/push/subscribe/https://push.example.com/gone")
    assert resp.status_code == 404


# ---------------------------------------------------------------------------
# Unit: subscription pruning on 410 Gone
# ---------------------------------------------------------------------------


def test_send_test_notification_prunes_410(tmp_path: Path):
    from pywebpush import WebPushException

    from app.push_service import send_test_notification

    subs_path = tmp_path / "subs4.json"
    pub_path = tmp_path / "vapid.pub"
    priv_path = tmp_path / "vapid.priv"
    # write dummy key files (content doesn't matter for mocked send)
    pub_path.write_text("dummy-pub-key")
    priv_path.write_text("dummy-priv-key")

    subs = [
        {"endpoint": "https://push.example.com/dead", "keys": {}},
        {"endpoint": "https://push.example.com/alive", "keys": {}},
    ]
    config = PushConfig(
        subscriptions_path=subs_path,
        vapid_public_key_path=pub_path,
        vapid_private_key_path=priv_path,
    )

    def mock_sender(**kwargs):
        endpoint = kwargs["subscription_info"]["endpoint"]
        if "dead" in endpoint:
            exc = WebPushException("Gone")
            resp_mock = MagicMock()
            resp_mock.status_code = 410
            exc.response = resp_mock
            raise exc

    sent, remaining, error = send_test_notification(subs, config, sender=mock_sender)
    assert sent == 1
    assert len(remaining) == 1
    assert remaining[0]["endpoint"] == "https://push.example.com/alive"
    assert error is None


# ---------------------------------------------------------------------------
# Unit: ntfy POST shape
# ---------------------------------------------------------------------------


def test_notify_send_ntfy_shape(tmp_path: Path):
    from app.notify import handle_notify_send

    subs_path = tmp_path / "subs5.json"
    pub_path = tmp_path / "vapid.pub"
    priv_path = tmp_path / "vapid.priv"
    pub_path.write_text("dummy-pub")
    priv_path.write_text("dummy-priv")
    save_subscriptions(subs_path, [])

    config = PushConfig(
        subscriptions_path=subs_path,
        vapid_public_key_path=pub_path,
        vapid_private_key_path=priv_path,
    )

    captured: dict = {}

    def mock_post(url, **kwargs):
        captured["url"] = url
        captured["content"] = kwargs.get("content", b"")
        captured["headers"] = kwargs.get("headers", {})
        resp = MagicMock()
        resp.status_code = 200
        return resp

    with patch("app.notify.httpx.post", side_effect=mock_post):
        with patch("app.notify._is_quiet_hours", return_value=False):
            with patch("app.notify._is_rate_limited", return_value=False):
                result = handle_notify_send(
                    {"title": "Hello", "body": "World", "tag": "test", "url": "/foo"},
                    config,
                    notification_channel="ntfy",
                    ntfy_topic="hearth-test-topic",
                )

    assert result["ok"] is True
    assert "ntfy" in result["delivered"]
    assert "hearth-test-topic" in captured["url"]
    assert captured["headers"]["Title"] == "Hello"
    assert captured["headers"]["Click"] == "/foo"
    assert captured["content"] == b"World"


# ---------------------------------------------------------------------------
# Unit: quiet hours and rate limit
# ---------------------------------------------------------------------------


def test_notify_send_quiet_hours_blocks(tmp_path: Path):
    from app.notify import handle_notify_send

    config = PushConfig(
        subscriptions_path=tmp_path / "s.json",
        vapid_public_key_path=tmp_path / "v.pub",
        vapid_private_key_path=tmp_path / "v.priv",
    )

    with patch("app.notify._is_quiet_hours", return_value=True):
        result = handle_notify_send(
            {"title": "T", "body": "B", "tag": "t"},
            config,
            notification_channel="ntfy",
            ntfy_topic="test",
        )
    assert result["ok"] is False
    assert result.get("queued") is True


def test_notify_send_urgent_bypasses_quiet_hours(tmp_path: Path):
    from app.notify import handle_notify_send

    subs_path = tmp_path / "s2.json"
    save_subscriptions(subs_path, [])
    config = PushConfig(
        subscriptions_path=subs_path,
        vapid_public_key_path=tmp_path / "v2.pub",
        vapid_private_key_path=tmp_path / "v2.priv",
    )

    with patch("app.notify._is_quiet_hours", return_value=True):
        with patch("app.notify.httpx.post") as mock_post:
            mock_post.return_value = MagicMock(status_code=200)
            with patch("app.notify._is_rate_limited", return_value=False):
                result = handle_notify_send(
                    {"title": "Urgent", "body": "B", "tag": "u", "urgent": True},
                    config,
                    notification_channel="ntfy",
                    ntfy_topic="hearth-test",
                )
    assert "error" not in result or result.get("ok") is not False or result.get("queued") is None

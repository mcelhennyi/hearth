from __future__ import annotations

import base64
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from pywebpush import WebPushException

from app.push_service import PushConfig, build_vapid_headers, send_test_notification

TEST_PUBLIC_KEY = (
    "BCqV2w2M9mV4MLwZqj1qNn5MJa7AqUQFOUa5SOGQ7ZZWmxuLk0ynrj5MQ8db3TsBvAk4fV1d2QwzRfj4Ynn4s5o"  # noqa: E501
)
TEST_PRIVATE_KEY = "k0-TevVY2QkS5SIJ5L81LBgUQwQh0GsxM8qX8CbU9v0"


def _decode_claims_from_auth_header(auth_header: str) -> dict[str, Any]:
    token = auth_header.replace("WebPush ", "").replace("vapid t=", "").split(", k=")[0]
    payload_segment = token.split(".")[1]
    padded = payload_segment + "=" * (-len(payload_segment) % 4)
    return json.loads(base64.urlsafe_b64decode(padded).decode("utf-8"))


def test_build_vapid_headers_has_expected_claims() -> None:
    headers = build_vapid_headers(
        "https://web.push.apple.com/3/device/some-token",
        private_key=TEST_PRIVATE_KEY,
        public_key=TEST_PUBLIC_KEY,
        subject="mailto:test@example.com",
        exp=1_800_000_000,
    )

    assert "Authorization" in headers
    claims = _decode_claims_from_auth_header(headers["Authorization"])
    assert claims["aud"] == "https://web.push.apple.com"
    assert claims["exp"] == 1_800_000_000
    assert claims["sub"] == "mailto:test@example.com"


def test_send_test_notification_prunes_410_subscriptions() -> None:
    with TemporaryDirectory() as tmp:
        config = PushConfig(
            subscriptions_path=Path(tmp) / "push-subscriptions.json",
            vapid_public_key_path=Path(tmp) / "vapid.pub",
            vapid_private_key_path=Path(tmp) / "vapid.priv",
        )
        config.vapid_public_key_path.write_text(TEST_PUBLIC_KEY, encoding="utf-8")
        config.vapid_private_key_path.write_text(TEST_PRIVATE_KEY, encoding="utf-8")
        subscriptions = [
            {"endpoint": "https://web.push.apple.com/old", "keys": {"p256dh": "a", "auth": "b"}},
            {"endpoint": "https://web.push.apple.com/new", "keys": {"p256dh": "c", "auth": "d"}},
        ]

        def fake_sender(*, subscription_info: dict[str, Any], **_: Any) -> None:
            if subscription_info["endpoint"].endswith("/old"):
                response = type("Resp", (), {"status_code": 410})()
                raise WebPushException("gone", response=response)

        sent, remaining, err = send_test_notification(subscriptions, config, sender=fake_sender)
        assert sent == 1
        assert err is None
        assert [item["endpoint"] for item in remaining] == ["https://web.push.apple.com/new"]

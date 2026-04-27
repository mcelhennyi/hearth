from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from fastapi.testclient import TestClient
from pywebpush import WebPushException

from app.main import app
from app.push_service import PushConfig

TEST_PUBLIC_KEY = "BCqV2w2M9mV4MLwZqj1qNn5MJa7AqUQFOUa5SOGQ7ZZWmxuLk0ynrj5MQ8db3TsBvAk4fV1d2QwzRfj4Ynn4s5o"
TEST_PRIVATE_KEY = "k0-TevVY2QkS5SIJ5L81LBgUQwQh0GsxM8qX8CbU9v0"


def test_push_test_endpoint_sends_to_all_and_prunes_410(monkeypatch: Any) -> None:
    with TemporaryDirectory() as tmp:
        config = PushConfig(
            subscriptions_path=Path(tmp) / "push-subscriptions.json",
            vapid_public_key_path=Path(tmp) / "vapid.pub",
            vapid_private_key_path=Path(tmp) / "vapid.priv",
        )
        config.vapid_public_key_path.write_text(TEST_PUBLIC_KEY, encoding="utf-8")
        config.vapid_private_key_path.write_text(TEST_PRIVATE_KEY, encoding="utf-8")
        config.subscriptions_path.write_text(
            json.dumps(
                [
                    {"endpoint": "https://web.push.apple.com/gone", "keys": {"p256dh": "a", "auth": "b"}},
                    {"endpoint": "https://web.push.apple.com/live", "keys": {"p256dh": "c", "auth": "d"}},
                ]
            ),
            encoding="utf-8",
        )

        app.state.push_config = config
        sent_endpoints: list[str] = []

        def fake_sender(*, subscription_info: dict[str, Any], **_: Any) -> None:
            sent_endpoints.append(subscription_info["endpoint"])
            if subscription_info["endpoint"].endswith("/gone"):
                response = type("Resp", (), {"status_code": 410})()
                raise WebPushException("gone", response=response)

        monkeypatch.setattr("app.push_service.webpush", fake_sender)

        client = TestClient(app)
        response = client.post("/api/push/test")
        assert response.status_code == 200
        assert response.json() == {"attempted": 2, "sent": 1, "remaining": 1}
        assert sent_endpoints == [
            "https://web.push.apple.com/gone",
            "https://web.push.apple.com/live",
        ]

        stored = json.loads(config.subscriptions_path.read_text(encoding="utf-8"))
        assert [item["endpoint"] for item in stored] == ["https://web.push.apple.com/live"]

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlparse

from py_vapid import Vapid01
from pywebpush import WebPushException, webpush


@dataclass(frozen=True)
class PushConfig:
    subscriptions_path: Path
    vapid_public_key_path: Path
    vapid_private_key_path: Path
    vapid_subject: str = "mailto:hearth@example.com"


def load_vapid_keys(config: PushConfig) -> tuple[str, str]:
    public = config.vapid_public_key_path.read_text(encoding="utf-8").strip()
    private = config.vapid_private_key_path.read_text(encoding="utf-8").strip()
    return public, private


def get_audience(endpoint: str) -> str:
    parsed = urlparse(endpoint)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("invalid push endpoint")
    return f"{parsed.scheme}://{parsed.netloc}"


def build_vapid_claims(endpoint: str, subject: str, exp: int | None = None) -> dict[str, Any]:
    claims: dict[str, Any] = {"sub": subject, "aud": get_audience(endpoint)}
    if exp is not None:
        claims["exp"] = exp
    return claims


def build_vapid_headers(
    endpoint: str, *, private_key: str, public_key: str, subject: str, exp: int | None = None
) -> dict[str, str]:
    claims = build_vapid_claims(endpoint, subject, exp)
    vapid = Vapid01.from_string(private_key)
    return vapid.sign(claims)


def send_test_notification(
    subscriptions: list[dict[str, Any]],
    config: PushConfig,
    sender: Callable[..., Any] | None = None,
) -> tuple[int, list[dict[str, Any]]]:
    sender_fn = sender or webpush
    _, private_key = load_vapid_keys(config)
    payload = json.dumps({"title": "Hearth test", "body": "Push path is working.", "url": "/"})

    sent_count = 0
    remaining: list[dict[str, Any]] = []
    for subscription in subscriptions:
        try:
            sender_fn(
                subscription_info=subscription,
                data=payload,
                vapid_private_key=private_key,
                vapid_claims=build_vapid_claims(subscription["endpoint"], config.vapid_subject),
            )
            sent_count += 1
            remaining.append(subscription)
        except WebPushException as exc:
            status_code = getattr(getattr(exc, "response", None), "status_code", None)
            if status_code == 410:
                continue
            raise
    return sent_count, remaining

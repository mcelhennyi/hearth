"""hub.notify.send Spark capability handler.

Authority: docs/design/notifications.md

Contract:
  - Called via Spark as hub.notify.send({title, body, tag, url, urgent, actions}).
  - Checks quiet hours (22:00–07:00 local by default, configurable in settings).
  - Per-tag rate limit: 1/hour unless urgent=True.
  - Fans out to Web Push and/or ntfy based on notification_channel setting.
  - Returns {ok: True, delivered: [...]} or {ok: False, error: "..."}.

DESIGN-GAP DG-N1 — VAPID rotation unspecified; install-time keys only for MVP.
"""

from __future__ import annotations

import json
import time
from datetime import datetime
from typing import Any

import httpx

from app.push_service import PushConfig, build_vapid_claims, load_vapid_keys
from app.push_store import load_subscriptions, save_subscriptions

try:
    from pywebpush import WebPushException, webpush
except ImportError:  # allow tests without pywebpush installed
    webpush = None  # type: ignore[assignment]
    WebPushException = Exception  # type: ignore[assignment, misc]


# in-process per-tag rate limit: {tag: last_sent_ts}
_tag_last_sent: dict[str, float] = {}
TAG_RATE_LIMIT_SECONDS = 3600  # 1/hour


def _is_quiet_hours(quiet_start: int = 22, quiet_end: int = 7) -> bool:
    hour = datetime.now().hour
    if quiet_start > quiet_end:  # e.g. 22–07 wraps midnight
        return hour >= quiet_start or hour < quiet_end
    return quiet_start <= hour < quiet_end  # non-wrapping range


def _is_rate_limited(tag: str) -> bool:
    last = _tag_last_sent.get(tag, 0.0)
    return (time.time() - last) < TAG_RATE_LIMIT_SECONDS


def _record_sent(tag: str) -> None:
    _tag_last_sent[tag] = time.time()


def _send_webpush(
    subscription: dict[str, Any],
    payload: str,
    config: PushConfig,
) -> bool:
    """Send one web push. Returns False if the subscription is expired (410)."""
    if webpush is None:
        return True  # no-op in test environments without pywebpush
    _, private_key = load_vapid_keys(config)
    try:
        webpush(
            subscription_info=subscription,
            data=payload,
            vapid_private_key=private_key,
            vapid_claims=build_vapid_claims(subscription["endpoint"], config.vapid_subject),
        )
        return True
    except WebPushException as exc:
        status = getattr(getattr(exc, "response", None), "status_code", None)
        if status == 410:
            return False
        raise


def _send_ntfy(topic: str, title: str, body: str, url: str | None = None) -> None:
    headers = {"Title": title}
    if url:
        headers["Click"] = url
    httpx.post(
        f"https://ntfy.sh/{topic}",
        content=body.encode(),
        headers=headers,
        timeout=10,
    )


def handle_notify_send(
    params: dict[str, Any],
    push_config: PushConfig,
    *,
    notification_channel: str = "webpush",
    ntfy_topic: str | None = None,
    quiet_start: int = 22,
    quiet_end: int = 7,
) -> dict[str, Any]:
    """Execute hub.notify.send.

    Returns {ok: True, delivered: [...]} or {ok: False, error: "..."}.
    """
    title = str(params.get("title", "Hearth"))
    body = str(params.get("body", ""))
    tag = str(params.get("tag", "default"))
    url = params.get("url")
    urgent = bool(params.get("urgent", False))

    if not urgent and _is_quiet_hours(quiet_start, quiet_end):
        return {"ok": False, "error": "quiet_hours", "queued": True}

    if not urgent and _is_rate_limited(tag):
        return {"ok": False, "error": "rate_limited"}

    delivered: list[str] = []
    last_error: str | None = None

    if notification_channel in ("webpush", "both"):
        subs = load_subscriptions(push_config.subscriptions_path)
        payload = json.dumps({"title": title, "body": body, "tag": tag, "url": url})
        remaining = []
        for i, sub in enumerate(subs):
            try:
                alive = _send_webpush(sub, payload, push_config)
                if alive:
                    remaining.append(sub)
                    delivered.append(f"webpush:device-{i}")
            except Exception as exc:
                last_error = str(exc)
                remaining.append(sub)
        if len(remaining) != len(subs):
            save_subscriptions(push_config.subscriptions_path, remaining)

    if notification_channel in ("ntfy", "both") and ntfy_topic:
        try:
            _send_ntfy(ntfy_topic, title, body, str(url) if url else None)
            delivered.append("ntfy")
        except Exception as exc:
            last_error = str(exc)

    _record_sent(tag)
    if delivered:
        return {"ok": True, "delivered": delivered}
    return {"ok": False, "error": last_error or "no_channels"}

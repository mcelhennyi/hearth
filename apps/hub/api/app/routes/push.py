"""Web Push routes — subscribe, unsubscribe, VAPID public key, test send.

Authority: docs/design/notifications.md
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException, Request

from app.push_service import PushConfig, send_test_notification
from app.push_store import load_subscriptions, save_subscriptions, upsert_subscription

router = APIRouter(prefix="/api/push", tags=["push"])

_default_subs_dir = Path(os.getenv("HEARTH_VAR_DIR", "var/hearth"))


def _push_config(request: Request) -> PushConfig:
    cfg: PushConfig | None = getattr(request.app.state, "push_config", None)
    if cfg is None:
        raise HTTPException(status_code=503, detail="Push not configured.")
    return cfg


@router.post("/subscribe")
def subscribe(subscription: dict[str, Any], request: Request) -> dict[str, int]:
    config = _push_config(request)
    try:
        subscriptions = load_subscriptions(config.subscriptions_path)
        subscriptions = upsert_subscription(subscriptions, subscription)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    save_subscriptions(config.subscriptions_path, subscriptions)
    return {"stored": len(subscriptions)}


@router.delete("/subscribe/{endpoint:path}")
def unsubscribe(endpoint: str, request: Request) -> dict[str, int]:
    config = _push_config(request)
    subscriptions = load_subscriptions(config.subscriptions_path)
    remaining = [s for s in subscriptions if s.get("endpoint") != endpoint]
    if len(remaining) == len(subscriptions):
        raise HTTPException(status_code=404, detail="Subscription not found.")
    save_subscriptions(config.subscriptions_path, remaining)
    return {"stored": len(remaining)}


@router.get("/vapid-public-key")
def vapid_public_key(request: Request) -> dict[str, str]:
    config = _push_config(request)
    try:
        public_key = config.vapid_public_key_path.read_text(encoding="utf-8").strip()
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail="VAPID public key not found. Run ./develop vapid-gen.",
        ) from exc
    if not public_key:
        raise HTTPException(status_code=500, detail="VAPID public key is empty.")
    return {"publicKey": public_key}


@router.post("/test")
def push_test(request: Request) -> dict[str, int | str | None]:
    config = _push_config(request)
    subscriptions = load_subscriptions(config.subscriptions_path)
    if not subscriptions:
        raise HTTPException(
            status_code=400,
            detail="No push subscriptions stored.",
        )
    try:
        sent, remaining, last_error = send_test_notification(subscriptions, config)
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=503,
            detail="VAPID keys missing. Run hearth pwa vapid-gen or ./develop vapid-gen.",
        ) from exc
    except OSError as exc:
        raise HTTPException(status_code=500, detail=f"Failed to read VAPID keys: {exc}") from exc
    if len(remaining) != len(subscriptions):
        save_subscriptions(config.subscriptions_path, remaining)
    return {
        "attempted": len(subscriptions),
        "sent": sent,
        "remaining": len(remaining),
        "error": last_error,
    }

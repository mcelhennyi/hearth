from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException

from .push_service import PushConfig, send_test_notification
from .push_store import load_subscriptions, save_subscriptions, upsert_subscription

DEFAULT_VAR_DIR = Path(os.getenv("HEARTH_VAR_DIR", "/workspace/var/hearth"))
DEFAULT_PUSH_CONFIG = PushConfig(
    subscriptions_path=Path(os.getenv("HEARTH_PUSH_SUBSCRIPTIONS_PATH", str(DEFAULT_VAR_DIR / "push-subscriptions.json"))),
    vapid_public_key_path=Path(os.getenv("HEARTH_VAPID_PUBLIC_KEY_PATH", str(DEFAULT_VAR_DIR / "secrets" / "vapid.pub"))),
    vapid_private_key_path=Path(os.getenv("HEARTH_VAPID_PRIVATE_KEY_PATH", str(DEFAULT_VAR_DIR / "secrets" / "vapid.priv"))),
)

app = FastAPI(title="Hearth Hub API")
app.state.push_config = DEFAULT_PUSH_CONFIG


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/push/subscribe")
def subscribe(subscription: dict[str, Any]) -> dict[str, int]:
    config: PushConfig = app.state.push_config
    try:
        subscriptions = load_subscriptions(config.subscriptions_path)
        subscriptions = upsert_subscription(subscriptions, subscription)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    save_subscriptions(config.subscriptions_path, subscriptions)
    return {"stored": len(subscriptions)}


@app.get("/api/push/vapid-public-key")
def vapid_public_key() -> dict[str, str]:
    config: PushConfig = app.state.push_config
    try:
        public_key = config.vapid_public_key_path.read_text(encoding="utf-8").strip()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="VAPID public key not found. Run ./develop vapid-gen.") from exc
    if not public_key:
        raise HTTPException(status_code=500, detail="VAPID public key is empty.")
    return {"publicKey": public_key}


@app.post("/api/push/test")
def push_test() -> dict[str, int]:
    config: PushConfig = app.state.push_config
    subscriptions = load_subscriptions(config.subscriptions_path)
    sent, remaining = send_test_notification(subscriptions, config)
    if len(remaining) != len(subscriptions):
        save_subscriptions(config.subscriptions_path, remaining)
    return {"attempted": len(subscriptions), "sent": sent, "remaining": len(remaining)}

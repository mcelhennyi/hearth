"""Hearth Hub API — FastAPI application entry point.

Routes:
  /api/health          — liveness (routes/health.py)
  /api/plugins         — plugin registry CRUD (routes/plugins.py)
  /api/settings        — hub settings (routes/settings.py)
  /api/push/*          — web push (push_service.py) — retained from FR-0002

DB: async SQLite at HEARTH_VAR_DIR/hearth.db via db.py + Alembic migrations.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException

from .push_service import PushConfig, send_test_notification
from .push_store import load_subscriptions, save_subscriptions, upsert_subscription
from .routes.health import router as health_router
from .routes.plugins import router as plugins_router
from .routes.settings import router as settings_router

DEFAULT_VAR_DIR = Path(os.getenv("HEARTH_VAR_DIR", "/workspace/var/hearth"))
_default_subs = str(DEFAULT_VAR_DIR / "push-subscriptions.json")
DEFAULT_PUSH_CONFIG = PushConfig(
    subscriptions_path=Path(os.getenv("HEARTH_PUSH_SUBSCRIPTIONS_PATH", _default_subs)),
    vapid_public_key_path=Path(
        os.getenv("HEARTH_VAPID_PUBLIC_KEY_PATH", str(DEFAULT_VAR_DIR / "secrets" / "vapid.pub"))
    ),
    vapid_private_key_path=Path(
        os.getenv("HEARTH_VAPID_PRIVATE_KEY_PATH", str(DEFAULT_VAR_DIR / "secrets" / "vapid.priv"))
    ),
)

app = FastAPI(title="Hearth Hub API", docs_url="/api/docs", redoc_url="/api/redoc")
app.state.push_config = DEFAULT_PUSH_CONFIG

app.include_router(health_router)
app.include_router(plugins_router)
app.include_router(settings_router)


# ---------------------------------------------------------------------------
# Web Push routes — retained from FR-0002 (T-FR-0001-09 will reorganize)
# ---------------------------------------------------------------------------


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
        raise HTTPException(
            status_code=404,
            detail="VAPID public key not found. Run ./develop vapid-gen.",
        ) from exc
    if not public_key:
        raise HTTPException(status_code=500, detail="VAPID public key is empty.")
    return {"publicKey": public_key}


@app.post("/api/push/test")
def push_test() -> dict[str, int | str | None]:
    config: PushConfig = app.state.push_config
    subscriptions = load_subscriptions(config.subscriptions_path)
    if not subscriptions:
        raise HTTPException(
            status_code=400,
            detail="No push subscriptions stored. Allow notifications in the PWA, then try again.",
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
    body: dict[str, int | str | None] = {
        "attempted": len(subscriptions),
        "sent": sent,
        "remaining": len(remaining),
        "error": last_error,
    }
    return body

"""Hearth Hub API — FastAPI application entry point.

Routes:
  /api/health          — liveness (routes/health.py)
  /api/plugins         — plugin registry CRUD (routes/plugins.py)
  /api/settings        — hub settings (routes/settings.py)
  /api/auth/*          — single-user auth (routes/auth.py)
  /api/push/*          — web push subscribe/unsubscribe/test (routes/push.py)
  /api/system/*        — system tiles & strips (routes/system.py)
  /api/dashboard/layout — per-user dashboard grid (routes/dashboard.py)
  /api/user/preferences  — per-user theme & toggles (routes/user.py)

DB: async SQLite at HEARTH_VAR_DIR/hearth.db via db.py + Alembic migrations.
"""

from __future__ import annotations

import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from sqlalchemy import text

from . import auth_verify
from .builtins import register_builtin_plugins
from .db import _DEFAULT_VAR_DIR, _SessionFactory, engine
from .models import Base
from .push_service import PushConfig
from .routes.auth import router as auth_router
from .routes.dashboard import router as dashboard_router
from .routes.health import router as health_router
from .routes.plugins import router as plugins_router
from .routes.push import router as push_router
from .routes.settings import router as settings_router
from .routes.system import router as system_router
from .routes.user import router as user_router

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


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    _DEFAULT_VAR_DIR.mkdir(parents=True, exist_ok=True)
    auth_verify.load_or_create_user_sig_secret()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        columns = await conn.execute(text("PRAGMA table_info(plugins)"))
        if "builtin" not in {row[1] for row in columns}:
            await conn.execute(
                text("ALTER TABLE plugins ADD COLUMN builtin BOOLEAN NOT NULL DEFAULT 0")
            )
    async with _SessionFactory() as session:
        await register_builtin_plugins(session)
    yield


app = FastAPI(
    title="Hearth Hub API",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan,
)
app.state.push_config = DEFAULT_PUSH_CONFIG

app.include_router(health_router)
app.include_router(plugins_router)
app.include_router(settings_router)
app.include_router(auth_router)
app.include_router(push_router)
app.include_router(system_router)
app.include_router(dashboard_router)
app.include_router(user_router)

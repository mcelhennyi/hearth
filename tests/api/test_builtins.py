"""Built-in plugin registry behavior for FR-0004."""

from __future__ import annotations

import asyncio
from pathlib import Path

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.builtins import register_builtin_plugins
from app.models import Base, Plugin

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_register_builtin_plugins_installs_hearth_users() -> None:
    async def _run() -> None:
        engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
        factory = async_sessionmaker(engine, expire_on_commit=False)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        async with factory() as session:
            await register_builtin_plugins(
                session,
                builtin_root=REPO_ROOT / "apps" / "builtin",
            )
            plugin = await session.get(Plugin, "hearth-users")
            assert plugin is not None
            assert plugin.builtin is True
            assert plugin.state == "enabled"
            assert plugin.kind == "app"

        await engine.dispose()

    asyncio.run(_run())


def test_builtin_plugin_cannot_be_uninstalled(client: TestClient) -> None:
    install = client.post(
        "/api/plugins/install",
        json={"source": "apps/builtin/hearth-users"},
    )
    assert install.status_code == 200
    assert install.json()["builtin"] is True

    uninstall = client.post("/api/plugins/hearth-users/uninstall")
    assert uninstall.status_code == 403
    assert "built-in" in uninstall.json()["detail"]

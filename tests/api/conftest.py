"""Shared fixtures for Hub API tests (T-FR-0001-02).

Uses a per-test in-memory SQLite database injected via FastAPI's dependency
override mechanism. Tests are synchronous (FastAPI TestClient handles the
async event loop internally).
"""
from __future__ import annotations

import asyncio
from collections.abc import AsyncGenerator, Generator
from typing import Any

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db import get_session
from app.main import app
from app import models_dashboard, models_user  # noqa: F401 — register ORM tables
from app.models import Base

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_engine_and_factory(db_url: str = "sqlite+aiosqlite:///:memory:") -> tuple[Any, Any]:
    engine = create_async_engine(db_url, echo=False)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    return engine, factory


def _sync_run(coro: Any) -> Any:
    """Run a coroutine synchronously, creating a temporary event loop if needed."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            raise RuntimeError("closed")
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    """Test client with a fresh in-memory SQLite DB per test.

    Creates tables, injects session override, tears down after the test.
    """
    engine, factory = _make_engine_and_factory()

    # Create tables synchronously before the test runs
    async def _create_tables() -> None:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    _sync_run(_create_tables())

    # Hold a single session open for the lifetime of this test so that
    # all requests within the same TestClient share one transaction view.
    session: AsyncSession = factory()

    async def _override_get_session() -> AsyncGenerator[AsyncSession, None]:
        yield session

    app.dependency_overrides[get_session] = _override_get_session

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.pop(get_session, None)

    async def _teardown() -> None:
        await session.close()
        await engine.dispose()

    _sync_run(_teardown())

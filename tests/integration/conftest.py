"""Fixtures for integration tests under tests/integration/.

Provides the same ``client`` TestClient fixture as tests/api/conftest.py
so unit-level install tests can run here without the full Compose stack.
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
from app.models import Base


def _make_engine_and_factory(db_url: str = "sqlite+aiosqlite:///:memory:") -> tuple[Any, Any]:
    engine = create_async_engine(db_url, echo=False)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    return engine, factory


def _sync_run(coro: Any) -> Any:
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            raise RuntimeError("closed")
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    engine, factory = _make_engine_and_factory()

    async def _create_tables() -> None:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    _sync_run(_create_tables())

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

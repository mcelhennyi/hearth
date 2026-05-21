"""Async SQLite engine and session factory for the Hearth hub API.

The DB path defaults to ``var/hearth/hearth.db`` under ``HEARTH_VAR_DIR``
(absolute) or under the repository workspace root when running inside Docker
(``/workspace/var/hearth/hearth.db``).

Tests override ``get_session`` via FastAPI dependency injection; see
``tests/api/conftest.py``.
"""

from __future__ import annotations

import os
from collections.abc import AsyncGenerator
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

_DEFAULT_VAR_DIR = Path(os.getenv("HEARTH_VAR_DIR", "/workspace/var/hearth"))
_DEFAULT_DB_PATH = _DEFAULT_VAR_DIR / "hearth.db"

_DB_URL = os.getenv(
    "HEARTH_DB_URL",
    f"sqlite+aiosqlite:///{_DEFAULT_DB_PATH}",
)

engine = create_async_engine(_DB_URL, echo=False)
_SessionFactory: async_sessionmaker[AsyncSession] = async_sessionmaker(
    engine, expire_on_commit=False
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency: yield one DB session per request."""
    async with _SessionFactory() as session:
        yield session

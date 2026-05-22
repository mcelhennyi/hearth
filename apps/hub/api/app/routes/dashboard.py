"""Dashboard layout API — T-FR-0006-02.

GET  /api/dashboard/layout → DashboardLayout (default when none persisted).
PUT  /api/dashboard/layout → 200 on save, 409 on collision, 422 on schema invalid.

Authority: docs/design/dashboard.md § Layout persistence, § Default layout.

MVP single-user: rows are keyed by user_id == "local".
"""

from __future__ import annotations

from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

# Import models_dashboard so the table registers on app.models.Base.metadata.
from app import models_dashboard  # noqa: F401
from app.dashboard import (
    build_default_layout,
    find_collision,
    get_system_tiles_for_user,
    list_enabled_app_plugins,
)
from app.db import get_session
from app.models_dashboard import DashboardLayout
from app.schemas_dashboard import DashboardLayoutBody, DashboardLayoutResponse

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

# MVP: single-user — every request hits the same row.
_MVP_USER_ID = "local"


@router.get("/layout", response_model=DashboardLayoutResponse)
async def get_layout(session: AsyncSession = Depends(get_session)) -> DashboardLayoutResponse:
    row = await session.get(DashboardLayout, _MVP_USER_ID)
    if row is not None:
        return DashboardLayoutResponse(
            version=row.version,
            columns=row.columns,
            blocks=row.blocks,
            updated_at=row.updated_at,
        )
    # No saved layout — synthesize a default from current enabled plugins.
    enabled = await list_enabled_app_plugins(session)
    tiles = get_system_tiles_for_user(_MVP_USER_ID)
    default = build_default_layout(
        enabled_app_slugs=[p.slug for p in enabled],
        system_tile_ids=[t.get("id", "") for t in tiles],
    )
    return DashboardLayoutResponse(**default)


@router.put("/layout", response_model=DashboardLayoutResponse)
async def put_layout(
    body: DashboardLayoutBody,
    session: AsyncSession = Depends(get_session),
) -> DashboardLayoutResponse:
    block_dicts = [b.model_dump(exclude_none=True) for b in body.blocks]
    collision = find_collision(block_dicts)
    if collision is not None:
        a, b = collision
        raise HTTPException(
            status_code=409,
            detail=f"Block collision: '{a}' overlaps '{b}'.",
        )

    now = datetime.now(UTC)
    row = await session.get(DashboardLayout, _MVP_USER_ID)
    if row is None:
        row = DashboardLayout(
            user_id=_MVP_USER_ID,
            version=body.version,
            columns=body.columns,
            blocks=block_dicts,
            updated_at=now,
        )
        session.add(row)
    else:
        row.version = body.version
        row.columns = body.columns
        row.blocks = block_dicts
        row.updated_at = now
    await session.commit()
    await session.refresh(row)
    return DashboardLayoutResponse(
        version=row.version,
        columns=row.columns,
        blocks=row.blocks,
        updated_at=row.updated_at,
    )

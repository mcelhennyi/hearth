"""GET/POST /api/system/* — system tiles and strips — T-FR-0006-01.

Authority: docs/design/dashboard.md §DF-U1, §DF-U2.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.schemas.system import SystemStripResponse, SystemTilesResponse
from app.system_strips import dismiss_strip, select_strip
from app.system_tiles import list_tiles, set_tile_hidden

router = APIRouter(prefix="/api/system", tags=["system"])


# ---------------------------------------------------------------------------
# Tiles
# ---------------------------------------------------------------------------


@router.get("/tiles", response_model=SystemTilesResponse)
async def get_tiles(
    session: AsyncSession = Depends(get_session),
) -> SystemTilesResponse:
    tiles = await list_tiles(session)
    return SystemTilesResponse(tiles=tiles)


@router.post("/tiles/{tile_id}/hide", status_code=204)
async def hide_tile(
    tile_id: str, session: AsyncSession = Depends(get_session)
) -> Response:
    if not await set_tile_hidden(session, tile_id, hidden=True):
        raise HTTPException(status_code=404, detail=f"Unknown tile '{tile_id}'.")
    return Response(status_code=204)


@router.post("/tiles/{tile_id}/restore", status_code=204)
async def restore_tile(
    tile_id: str, session: AsyncSession = Depends(get_session)
) -> Response:
    if not await set_tile_hidden(session, tile_id, hidden=False):
        raise HTTPException(status_code=404, detail=f"Unknown tile '{tile_id}'.")
    return Response(status_code=204)


# ---------------------------------------------------------------------------
# Strips
# ---------------------------------------------------------------------------


@router.get("/strips", response_model=SystemStripResponse)
async def get_strip(
    platform: str | None = None,
    session: AsyncSession = Depends(get_session),
) -> SystemStripResponse:
    """Return the highest-priority active strip for the given client platform.

    ``platform`` is supplied by the client (``ios`` | ``android`` | ``desktop``).
    When omitted, no strip is served — every strip is platform-gated by design.
    """
    strip = await select_strip(session, platform)
    return SystemStripResponse(strip=strip)


@router.post("/strips/{strip_id}/dismiss", status_code=204)
async def dismiss(
    strip_id: str, session: AsyncSession = Depends(get_session)
) -> Response:
    if not await dismiss_strip(session, strip_id):
        raise HTTPException(status_code=404, detail=f"Unknown strip '{strip_id}'.")
    return Response(status_code=204)

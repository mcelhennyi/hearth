"""System tile catalogue and hide/restore helpers — T-FR-0006-01.

v0 tiles (authority: docs/design/dashboard.md §DF-U1):

  ca-trust    "Trust local CA"  → opens Settings → Trust CA
  hub-healthy "Hub healthy"     → /settings#diagnostics
  pi-online   "Hub online"      → /settings#diagnostics

Tiles in v0 are hard-coded; per-user hide state lives in
``user_system_state`` (scope='tile'). Tile self-suppression is deferred to the
client (the server reports ``suppressed=False`` for every tile and lets the
shell decide based on live state such as CA trust status).
"""

from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import UserSystemState
from app.schemas.system import SystemTile, TileAction


@dataclass(frozen=True)
class _TileDef:
    id: str
    title: str
    body: str
    nav: str | None


# Order is the canonical render order for the default layout.
V0_TILES: tuple[_TileDef, ...] = (
    _TileDef(
        id="ca-trust",
        title="Trust local CA",
        body=(
            "Install the Hearth root certificate to remove the iOS warning."
        ),
        nav="/settings#trust-ca",
    ),
    _TileDef(
        id="hub-healthy",
        title="Hub healthy",
        body="Compact status badge sourced from GET /api/health.",
        nav="/settings#diagnostics",
    ),
    _TileDef(
        id="pi-online",
        title="Hub online",
        body="Reachability and last-seen for the deployed hub (Pi or Mac).",
        nav="/settings#diagnostics",
    ),
)

V0_TILE_IDS: frozenset[str] = frozenset(t.id for t in V0_TILES)


def _to_tile(d: _TileDef, *, hidden: bool) -> SystemTile:
    return SystemTile(
        id=d.id,
        title=d.title,
        body=d.body,
        action=TileAction(nav=d.nav) if d.nav else None,
        hidden_by_user=hidden,
        suppressed=False,
    )


async def list_tiles(session: AsyncSession) -> list[SystemTile]:
    """Return the v0 tile catalogue with per-user hide state applied."""
    result = await session.execute(
        select(UserSystemState).where(UserSystemState.scope == "tile")
    )
    hidden_ids = {row.item_id for row in result.scalars().all() if row.hidden}
    return [_to_tile(t, hidden=t.id in hidden_ids) for t in V0_TILES]


async def set_tile_hidden(session: AsyncSession, tile_id: str, hidden: bool) -> bool:
    """Persist the hide/restore decision for one tile.

    Returns True when ``tile_id`` is known; False otherwise (caller maps to 404).
    Idempotent: re-hiding/re-restoring is a no-op.
    """
    if tile_id not in V0_TILE_IDS:
        return False
    row = await session.get(UserSystemState, ("tile", tile_id))
    if row is None:
        row = UserSystemState(scope="tile", item_id=tile_id, hidden=hidden)
        session.add(row)
    else:
        row.hidden = hidden
    await session.commit()
    return True

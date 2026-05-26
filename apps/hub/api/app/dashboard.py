"""Dashboard layout helpers — default generator and collision validator.

Authority: docs/design/dashboard.md § Default layout, § Layout persistence.

Default layout rules (mobile, columns = 4):
  1. One ``app-shortcut`` block (1x1) per enabled ``app`` plugin.
     Ordering: ``[ui.nav].order`` then ``name``. (Tinder manifest order data
     is not surfaced in the Plugin model in v0; we order by ``name`` for
     deterministic output and amend when nav order is available — DESIGN-GAP
     noted in ticket diary.)
  2. ``system`` tiles appended after shortcuts on the first row (wrap).
  3. No ``widget`` blocks in default (P3 deferred).

Collisions: any pair of blocks with overlapping (x,y,w,h) rectangles. Returns
True on first detected overlap (used by PUT /api/dashboard/layout to reject
with 409). Strip blocks are out of band — see schemas_dashboard.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Plugin

DEFAULT_COLUMNS = 4
DEFAULT_VERSION = 1


def get_system_tiles_for_user(user_id: str) -> list[dict[str, Any]]:
    """Stub until T-FR-0006-01 lands ``GET /api/system/tiles``.

    Returns the list of system tile descriptors that should appear in the
    default layout for ``user_id``. The real implementation will live in
    ``app/system_tiles.py`` (T-FR-0006-01).
    """
    # @PROJ-U-02 — replace with real source when system tiles ship.
    del user_id  # unused in stub
    return []


async def list_enabled_app_plugins(session: AsyncSession) -> list[Plugin]:
    """Return enabled plugins of kind=='app' ordered by name (deterministic)."""
    result = await session.execute(
        select(Plugin)
        .where(Plugin.state == "enabled", Plugin.kind == "app")
        .order_by(Plugin.name)
    )
    return list(result.scalars().all())


def _shortcut_block(plugin_slug: str, index: int, columns: int) -> dict[str, Any]:
    return {
        "id": f"default-shortcut-{plugin_slug}",
        "type": "app-shortcut",
        "plugin": plugin_slug,
        "x": index % columns,
        "y": index // columns,
        "w": 1,
        "h": 1,
    }


def _system_block(tile_id: str, index: int, columns: int) -> dict[str, Any]:
    return {
        "id": f"default-system-{tile_id}",
        "type": "system",
        "x": index % columns,
        "y": index // columns,
        "w": 1,
        "h": 1,
    }


def build_default_layout(
    enabled_app_slugs: Sequence[str],
    system_tile_ids: Sequence[str],
    columns: int = DEFAULT_COLUMNS,
) -> dict[str, Any]:
    """Compose a default layout per dashboard.md § Default layout.

    System tiles are appended after the app shortcuts on the first row and
    wrap naturally as the cursor advances.
    """
    blocks: list[dict[str, Any]] = []
    cursor = 0
    for slug in enabled_app_slugs:
        blocks.append(_shortcut_block(slug, cursor, columns))
        cursor += 1
    for tile_id in system_tile_ids:
        blocks.append(_system_block(tile_id, cursor, columns))
        cursor += 1
    return {
        "version": DEFAULT_VERSION,
        "columns": columns,
        "blocks": blocks,
    }


def find_collision(blocks: Iterable[dict[str, Any]]) -> tuple[str, str] | None:
    """Return ids of the first overlapping pair, or None.

    Rectangles are half-open: block at (x,y,w,h) covers cells
    ``x..x+w-1`` × ``y..y+h-1``.
    """
    materialized = list(blocks)
    for i, a in enumerate(materialized):
        ax, ay, aw, ah = a["x"], a["y"], a["w"], a["h"]
        for b in materialized[i + 1 :]:
            bx, by, bw, bh = b["x"], b["y"], b["w"], b["h"]
            if ax < bx + bw and bx < ax + aw and ay < by + bh and by < ay + ah:
                return str(a["id"]), str(b["id"])
    return None

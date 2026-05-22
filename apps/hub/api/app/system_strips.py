"""System strip catalogue and dismiss helpers — T-FR-0006-01.

v0 strips (authority: docs/design/dashboard.md §DF-U2):

  pwa-install   iOS Safari, not yet installed
  mac-shell     Desktop browser, no install hint

At most one strip is active at a time; the hub returns the highest-priority
non-dismissed strip whose platform matches. Platform detection is supplied by
the client via the ``platform`` query parameter
(``ios`` | ``android`` | ``desktop`` | ``unknown``).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import UserSystemState
from app.schemas.system import SystemStrip, TileAction


@dataclass(frozen=True)
class _StripDef:
    id: str
    title: str
    body: str
    nav: str | None
    platforms: frozenset[str]  # platforms where this strip is eligible
    priority: int               # lower number = higher priority


# Ordered by priority — the first non-dismissed eligible strip wins.
V0_STRIPS: tuple[_StripDef, ...] = (
    _StripDef(
        id="pwa-install",
        title="Install Hearth",
        body="Add Hearth to your Home Screen for the full app experience.",
        nav="/settings#install",
        platforms=frozenset({"ios"}),
        priority=10,
    ),
    _StripDef(
        id="mac-shell",
        title="Open Hearth in its own window",
        body=(
            "Install the desktop shell to use Hearth without a browser tab."
        ),
        nav="/settings#install",
        platforms=frozenset({"desktop"}),
        priority=20,
    ),
)

V0_STRIP_IDS: frozenset[str] = frozenset(s.id for s in V0_STRIPS)


def _to_strip(d: _StripDef, *, dismissed: bool) -> SystemStrip:
    return SystemStrip(
        id=d.id,
        title=d.title,
        body=d.body,
        action=TileAction(nav=d.nav) if d.nav else None,
        dismissed=dismissed,
    )


async def _dismissed_ids(session: AsyncSession) -> set[str]:
    result = await session.execute(
        select(UserSystemState).where(UserSystemState.scope == "strip")
    )
    return {
        row.item_id
        for row in result.scalars().all()
        if row.dismissed_at is not None
    }


async def select_strip(session: AsyncSession, platform: str | None) -> SystemStrip | None:
    """Return the single active strip for this platform, or None."""
    platform_key = (platform or "").lower()
    if not platform_key:
        # No platform hint → never serve a strip (each strip is platform-gated).
        return None
    dismissed = await _dismissed_ids(session)
    eligible = sorted(
        (s for s in V0_STRIPS if platform_key in s.platforms and s.id not in dismissed),
        key=lambda s: s.priority,
    )
    if not eligible:
        return None
    return _to_strip(eligible[0], dismissed=False)


async def dismiss_strip(session: AsyncSession, strip_id: str) -> bool:
    """Persist a dismissal for one strip.

    Returns True when ``strip_id`` is known; False otherwise (caller → 404).
    Idempotent: re-dismissing leaves the original timestamp in place.
    """
    if strip_id not in V0_STRIP_IDS:
        return False
    row = await session.get(UserSystemState, ("strip", strip_id))
    now = datetime.now(UTC)
    if row is None:
        row = UserSystemState(
            scope="strip", item_id=strip_id, hidden=False, dismissed_at=now
        )
        session.add(row)
    elif row.dismissed_at is None:
        row.dismissed_at = now
    await session.commit()
    return True

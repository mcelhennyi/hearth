"""Pydantic schemas for /api/system/{tiles,strips} — T-FR-0006-01.

Authority: docs/design/dashboard.md §"system block — content and configuration
(DF-U1)" and §"strip block — content and configuration (DF-U2)".
"""

from __future__ import annotations

from pydantic import BaseModel


class TileAction(BaseModel):
    """Tap action for a system tile — currently just a nav target."""

    nav: str


class SystemTile(BaseModel):
    id: str
    title: str
    body: str
    action: TileAction | None = None
    hidden_by_user: bool = False
    # Server-evaluated precondition (e.g. ca-trust hides once trust confirmed).
    # In v0 the server defers this to the client; always False.
    suppressed: bool = False


class SystemTilesResponse(BaseModel):
    tiles: list[SystemTile]


class SystemStrip(BaseModel):
    id: str
    title: str
    body: str
    action: TileAction | None = None
    dismissed: bool = False


class SystemStripResponse(BaseModel):
    strip: SystemStrip | None

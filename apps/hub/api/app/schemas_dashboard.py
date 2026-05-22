"""Pydantic schemas for the dashboard layout API.

Authority: docs/design/dashboard.md § Layout persistence.

Block shape (subset persisted in ``DashboardLayout.blocks``):

  - ``id``      stable identifier (uuid-ish string)
  - ``type``    one of ``app-shortcut`` | ``widget`` | ``system``
  - ``x``,``y`` origin in primitive cells (0-based)
  - ``w``,``h`` size in primitive cells (>= 1)
  - ``plugin``  required for ``app-shortcut`` and ``widget``
  - ``surface`` required for ``widget``

``strip`` blocks are NOT in ``blocks[]`` — strips render above the grid and
are served by the separate ``/api/system/strips`` surface (T-FR-0006-01).
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator

BlockType = Literal["app-shortcut", "widget", "system"]


class LayoutBlock(BaseModel):
    """One block in a saved layout. Strips are NOT represented here."""

    id: str = Field(min_length=1, max_length=128)
    type: BlockType
    x: int = Field(ge=0)
    y: int = Field(ge=0)
    w: int = Field(ge=1)
    h: int = Field(ge=1)
    plugin: str | None = None
    surface: str | None = None

    @model_validator(mode="after")
    def _type_required_fields(self) -> "LayoutBlock":
        if self.type == "app-shortcut" and not self.plugin:
            raise ValueError("app-shortcut block requires 'plugin'")
        if self.type == "widget":
            if not self.plugin:
                raise ValueError("widget block requires 'plugin'")
            if not self.surface:
                raise ValueError("widget block requires 'surface'")
        return self


class DashboardLayoutBody(BaseModel):
    """Request and response body for /api/dashboard/layout."""

    version: int = Field(default=1, ge=1)
    columns: int = Field(default=4, ge=1, le=32)
    blocks: list[LayoutBlock] = Field(default_factory=list)


class DashboardLayoutResponse(BaseModel):
    """Server response — passes blocks through as stored dicts (no None fill).

    Using ``list[dict]`` (vs ``list[LayoutBlock]``) preserves exactly what was
    persisted so PUT-then-GET round-trips without re-introducing optional
    ``None`` fields the client did not send.
    """

    version: int = Field(default=1, ge=1)
    columns: int = Field(default=4, ge=1, le=32)
    blocks: list[dict[str, Any]] = Field(default_factory=list)
    updated_at: datetime | None = None

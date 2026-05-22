"""Pydantic schemas for per-user preferences — T-FR-0006-04.

Authority: docs/design/mantle-ui.md § Settings modal, § Theme persistence.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

ThemePreference = Literal["light", "dark", "system"]


class UserPreferencesResponse(BaseModel):
    theme: ThemePreference = "system"


class UserPreferencesUpdateRequest(BaseModel):
    theme: ThemePreference | None = Field(default=None)

"""Pydantic request/response schemas for the Hearth hub API.

Authority: docs/design/plugin-contract.md
"""

from __future__ import annotations

import re
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, field_validator

SLUG_RE = re.compile(r"^[a-z][a-z0-9-]{0,31}$")

PluginState = Literal["disabled", "enabled", "uninstalled", "error"]
PluginKind = Literal["app", "widget", "service"]


class PluginInstallRequest(BaseModel):
    slug: str
    name: str
    version: str
    kind: PluginKind = "app"

    @field_validator("slug")
    @classmethod
    def slug_format(cls, v: str) -> str:
        if not SLUG_RE.match(v):
            raise ValueError(
                "slug must match ^[a-z][a-z0-9-]{0,31}$ (kebab-case ASCII, ≤ 32 chars)"
            )
        return v


class PluginResponse(BaseModel):
    slug: str
    name: str
    version: str
    kind: str
    state: str
    installed_at: datetime

    model_config = {"from_attributes": True}


class SettingsResponse(BaseModel):
    theme: str
    hostname: str
    notification_channel: str


class SettingsUpdateRequest(BaseModel):
    theme: str | None = None
    hostname: str | None = None
    notification_channel: str | None = None

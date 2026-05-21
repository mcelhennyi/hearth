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
    """Install a plugin by direct field values (backward-compat) or via a tinder.toml source path.

    When *source* is given, the Tinder loader validates tinder.toml and populates the other
    fields from the manifest. Explicit fields (slug/name/version/kind) are used only when
    *source* is absent (e.g. tests and CLI callers that pre-parse the manifest).
    """

    source: str | None = None  # path to plugin directory containing tinder.toml
    slug: str | None = None
    name: str | None = None
    version: str | None = None
    kind: PluginKind = "app"

    @field_validator("slug")
    @classmethod
    def slug_format(cls, v: str | None) -> str | None:
        if v is not None and not SLUG_RE.match(v):
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


class PluginInstallResponse(PluginResponse):
    """Superset of PluginResponse that also carries Tinder validation diagnostics.

    validation_errors is non-empty when the tinder.toml had issues but we still
    recorded the plugin row with state='disabled' per plugin-contract.md.
    """

    validation_errors: list[str] = []


class SettingsResponse(BaseModel):
    theme: str
    hostname: str
    notification_channel: str


class SettingsUpdateRequest(BaseModel):
    theme: str | None = None
    hostname: str | None = None
    notification_channel: str | None = None

"""Pydantic v2 models for tinder.toml — authoritative schema per docs/design/plugin-contract.md.

Validation rules: any failure raises ValueError with a human-readable message collected
by the loader; callers should never catch ValidationError directly.
"""

from __future__ import annotations

import re
from typing import Annotated, Any, Literal

from pydantic import BaseModel, Field, field_validator, model_validator

SLUG_RE = re.compile(r"^[a-z][a-z0-9-]{0,31}$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+")  # prefix match; full semver is complex enough

BackendKind = Literal["python", "node", "binary", "none"]
UiKind = Literal["static", "iframe-spa", "module-federation"]
NetworkKind = Literal["none", "loopback", "lan", "internet"]
PluginKind = Literal["app", "widget"]


class BackendConfig(BaseModel):
    kind: BackendKind
    module: str | None = None
    command: list[str] | None = None
    port_env: str | None = None


class UiConfig(BaseModel):
    kind: UiKind
    path: str | None = None
    base: str | None = None
    remote: str | None = None


class EntrypointConfig(BaseModel):
    backend: BackendConfig
    ui: UiConfig | None = None


class CapabilityBlock(BaseModel):
    methods: list[str] = Field(default_factory=list)
    events: list[str] = Field(default_factory=list)


class PermissionsBlock(BaseModel):
    spark_call: list[str] = Field(default_factory=list)
    spark_publish: list[str] = Field(default_factory=list)
    spark_subscribe: list[str] = Field(default_factory=list)
    fs_paths: list[str] = Field(default_factory=list)
    network: NetworkKind = "loopback"


class BackupBlock(BaseModel):
    include: list[str] = Field(default_factory=list)
    exclude: list[str] = Field(default_factory=list)


class NavBlock(BaseModel):
    label: str | None = None
    icon: str | None = None
    order: int = 50
    show_in_tab_bar: bool = True


class ChromeBlock(BaseModel):
    top: dict[str, Any] | None = None
    bottom: dict[str, Any] | None = None


class UiBlock(BaseModel):
    nav: NavBlock | None = None
    chrome: ChromeBlock | None = None


class PluginBlock(BaseModel):
    slug: Annotated[str, Field(min_length=1)]
    name: str
    version: str
    hearth_min: str = "0.1.0"
    kind: PluginKind = "app"
    description: str | None = None
    icon: str | None = None

    @field_validator("slug")
    @classmethod
    def slug_format(cls, v: str) -> str:
        if not SLUG_RE.match(v):
            raise ValueError(
                f"slug '{v}' must match ^[a-z][a-z0-9-]{{0,31}}$ (kebab-case ASCII, ≤ 32 chars)"
            )
        return v

    @field_validator("version", "hearth_min")
    @classmethod
    def semver_format(cls, v: str) -> str:
        if not SEMVER_RE.match(v):
            raise ValueError(f"'{v}' is not a valid semver string (e.g. 1.2.3)")
        return v


class WidgetSurface(BaseModel):
    title: str | None = None
    span_default: dict[str, Any] | None = None


class TinderManifest(BaseModel):
    """Root model for a validated tinder.toml."""

    plugin: PluginBlock
    entrypoint: EntrypointConfig
    capabilities: dict[str, CapabilityBlock] = Field(default_factory=dict)
    permissions: PermissionsBlock = Field(default_factory=PermissionsBlock)
    backup: BackupBlock = Field(default_factory=BackupBlock)
    ui: UiBlock = Field(default_factory=UiBlock)
    widget: dict[str, Any] | None = None  # widget.surfaces.<id> blocks

    @model_validator(mode="after")
    def validate_kind_constraints(self) -> TinderManifest:
        kind = self.plugin.kind
        ui = self.entrypoint.ui

        if kind == "app":
            if ui is None:
                raise ValueError(
                    "kind='app' requires [entrypoint.ui] (got none); "
                    'add ui = { kind = "static", path = "web/dist" } or similar'
                )
        elif kind == "widget":
            if ui is not None:
                raise ValueError(
                    "kind='widget' must not have [entrypoint.ui]; widgets have no full SPA route"
                )
            has_surfaces = (
                self.widget is not None
                and "surfaces" in self.widget
                and len(self.widget["surfaces"]) > 0
            )
            if not has_surfaces:
                raise ValueError("kind='widget' requires at least one [widget.surfaces.<id>] block")
        return self

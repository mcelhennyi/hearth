"""SQLAlchemy ORM models for the Hearth hub registry.

Tables:
  plugins   — plugin registry rows (one per installed slug)
  settings  — key/value store for hub-wide settings
  audit_log — append-only action log for plugin lifecycle events

Schema authority: docs/design/plugin-contract.md
"""

from __future__ import annotations

import re
from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, validates

SLUG_RE = re.compile(r"^[a-z][a-z0-9-]{0,31}$")

VALID_STATES = {"disabled", "enabled", "uninstalled", "error"}
VALID_KINDS = {"app", "widget", "service"}


class Base(DeclarativeBase):
    pass


class Plugin(Base):
    """One row per installed plugin slug.

    state lifecycle (stub — no supervisor calls in T-FR-0001-02):
      install  → disabled
      enable   → enabled  (widgets return 501 per MVP policy)
      disable  → disabled
      uninstall → uninstalled
    """

    __tablename__ = "plugins"

    slug: Mapped[str] = mapped_column(String(32), primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    version: Mapped[str] = mapped_column(String(64), nullable=False)
    kind: Mapped[str] = mapped_column(String(16), nullable=False, default="app")
    state: Mapped[str] = mapped_column(String(16), nullable=False, default="disabled")
    builtin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    installed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )

    @validates("slug")
    def validate_slug(self, _key: str, value: str) -> str:
        if not SLUG_RE.match(value):
            raise ValueError(f"Invalid slug {value!r}: must match ^[a-z][a-z0-9-]{{0,31}}$")
        return value

    @validates("state")
    def validate_state(self, _key: str, value: str) -> str:
        if value not in VALID_STATES:
            raise ValueError(f"Invalid state {value!r}: must be one of {VALID_STATES}")
        return value

    @validates("kind")
    def validate_kind(self, _key: str, value: str) -> str:
        if value not in VALID_KINDS:
            raise ValueError(f"Invalid kind {value!r}: must be one of {VALID_KINDS}")
        return value


class Setting(Base):
    """Hub-wide key/value settings store.

    Known keys (seeded on first access): theme, hostname, notification_channel.
    """

    __tablename__ = "settings"

    key: Mapped[str] = mapped_column(String(128), primary_key=True)
    value: Mapped[str] = mapped_column(Text, nullable=False)


class UserSystemState(Base):
    """Per-user (single-user v0) hide/dismiss state for system tiles and strips.

    Schema authority: docs/design/dashboard.md §DF-U1, §DF-U2.

      scope    "tile" | "strip"
      item_id  tile or strip id (e.g. "ca-trust", "pwa-install")
      hidden   True when tile is user-hidden (tiles only)
      dismissed_at  set when strip was dismissed (strips only)
    """

    __tablename__ = "user_system_state"

    scope: Mapped[str] = mapped_column(String(16), primary_key=True)
    item_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    hidden: Mapped[bool] = mapped_column(default=False, nullable=False)
    dismissed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )


class AuditLog(Base):
    """Append-only record of plugin lifecycle actions."""

    __tablename__ = "audit_log"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )
    action: Mapped[str] = mapped_column(String(32), nullable=False)
    plugin_slug: Mapped[str] = mapped_column(String(32), nullable=True)

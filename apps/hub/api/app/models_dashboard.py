"""SQLAlchemy model for the per-user dashboard layout.

Authority: docs/design/dashboard.md § Layout persistence.

One row per user (MVP: single local user identified by ``user_id`` string).
``blocks`` is stored as a JSON blob — schema validated by Pydantic on PUT.
"""

from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import JSON, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models import Base


class DashboardLayout(Base):
    """Persisted dashboard layout for one user.

    Columns:
      user_id     — single-user MVP uses ``"local"`` (single primary key).
      version     — layout schema version (currently always 1).
      columns     — column count for the saved layout (4 mobile, 8 desktop).
      blocks      — JSON list of block dicts (id/type/x/y/w/h/plugin/surface).
      updated_at  — last save time (UTC).
    """

    __tablename__ = "dashboard_layouts"

    user_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    columns: Mapped[int] = mapped_column(Integer, nullable=False, default=4)
    blocks: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )

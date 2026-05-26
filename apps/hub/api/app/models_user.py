"""SQLAlchemy model for per-user preferences — T-FR-0006-04.

Authority: docs/design/mantle-ui.md § Theme persistence.

MVP single-user: ``user_id`` is always ``"local"``.
"""

from __future__ import annotations

from app.models import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class UserPreferences(Base):
    """Persisted user preferences (theme and future toggles)."""

    __tablename__ = "user_preferences"

    user_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    theme: Mapped[str] = mapped_column(String(16), nullable=False, default="system")

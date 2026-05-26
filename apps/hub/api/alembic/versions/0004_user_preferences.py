"""Add user_preferences table — T-FR-0006-04.

Revision ID: 0004_user_preferences
Revises: 0003_dashboard_layouts
Create Date: 2026-05-21
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0004_user_preferences"
down_revision: str | None = "0003_dashboard_layouts"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "user_preferences",
        sa.Column("user_id", sa.String(64), primary_key=True),
        sa.Column("theme", sa.String(16), nullable=False, server_default="system"),
    )


def downgrade() -> None:
    op.drop_table("user_preferences")

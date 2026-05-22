"""Add dashboard_layouts table — T-FR-0006-02.

Revision ID: 0002_dashboard_layouts
Revises: 0001_init
Create Date: 2026-05-21
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0002_dashboard_layouts"
down_revision: str | None = "0001_init"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "dashboard_layouts",
        sa.Column("user_id", sa.String(64), primary_key=True),
        sa.Column("version", sa.Integer, nullable=False, server_default="1"),
        sa.Column("columns", sa.Integer, nullable=False, server_default="4"),
        sa.Column("blocks", sa.JSON, nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )


def downgrade() -> None:
    op.drop_table("dashboard_layouts")

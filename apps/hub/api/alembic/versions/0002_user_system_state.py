"""Add user_system_state table — T-FR-0006-01.

Stores per-user (single-user v0) hide state for system tiles and dismissal
state for system strips. Authority: docs/design/dashboard.md §DF-U1, §DF-U2.

Revision ID: 0002_user_system_state
Revises: 0001_init
Create Date: 2026-05-21
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0002_user_system_state"
down_revision: str | None = "0001_init"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "user_system_state",
        sa.Column("scope", sa.String(16), primary_key=True),
        sa.Column("item_id", sa.String(64), primary_key=True),
        sa.Column("hidden", sa.Boolean, nullable=False, server_default=sa.false()),
        sa.Column("dismissed_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("user_system_state")

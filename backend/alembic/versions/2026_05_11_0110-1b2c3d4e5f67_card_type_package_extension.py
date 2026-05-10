"""card type package extension

Revision ID: 1b2c3d4e5f67
Revises: 8f3b2a4d9b11
Create Date: 2026-05-11 01:10:00.000000+08:00
"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "1b2c3d4e5f67"
down_revision: str | Sequence[str] | None = "8f3b2a4d9b11"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("card_types", sa.Column("gift_amount_cents", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("card_types", sa.Column("purchase_limit", sa.Integer(), nullable=True))
    op.add_column("card_types", sa.Column("applicable_venue_ids", sa.String(length=255), nullable=True))
    op.add_column("card_types", sa.Column("sale_start_at", sa.Date(), nullable=True))
    op.add_column("card_types", sa.Column("sale_end_at", sa.Date(), nullable=True))
    op.add_column("card_types", sa.Column("package_kind", sa.String(length=40), nullable=True))
    op.create_index(op.f("ix_card_types_package_kind"), "card_types", ["package_kind"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_card_types_package_kind"), table_name="card_types")
    op.drop_column("card_types", "package_kind")
    op.drop_column("card_types", "sale_end_at")
    op.drop_column("card_types", "sale_start_at")
    op.drop_column("card_types", "applicable_venue_ids")
    op.drop_column("card_types", "purchase_limit")
    op.drop_column("card_types", "gift_amount_cents")

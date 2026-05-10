"""member and frontdesk extension

Revision ID: 8f3b2a4d9b11
Revises: ca9871597eb1
Create Date: 2026-05-11 00:30:00.000000+08:00
"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "8f3b2a4d9b11"
down_revision: str | Sequence[str] | None = "ca9871597eb1"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "members",
        sa.Column(
            "member_type",
            sa.Enum("REGULAR", "YEAR", "SEASON", "MONTH", "TIMES", "STORED_VALUE", "VIP", name="membertype", native_enum=False),
            nullable=False,
            server_default="REGULAR",
        ),
    )
    op.add_column("members", sa.Column("id_card_no", sa.String(length=32), nullable=True))
    op.add_column("members", sa.Column("wechat", sa.String(length=80), nullable=True))
    op.add_column("members", sa.Column("address", sa.String(length=255), nullable=True))
    op.add_column("members", sa.Column("tags", sa.Text(), nullable=True))
    op.create_index(op.f("ix_members_member_type"), "members", ["member_type"], unique=False)
    op.create_index(op.f("ix_members_id_card_no"), "members", ["id_card_no"], unique=False)

    op.add_column("member_profiles", sa.Column("id_card_front_url", sa.String(length=255), nullable=True))
    op.add_column("member_profiles", sa.Column("id_card_back_url", sa.String(length=255), nullable=True))

    op.alter_column("checkins", "member_id", existing_type=sa.Integer(), nullable=True)
    op.add_column(
        "checkins",
        sa.Column(
            "channel",
            sa.Enum("CARD", "QRCODE", "FACE", "VISITOR", name="checkinchannel", native_enum=False),
            nullable=False,
            server_default="CARD",
        ),
    )
    op.add_column("checkins", sa.Column("is_visitor", sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column("checkins", sa.Column("visitor_name", sa.String(length=80), nullable=True))
    op.add_column("checkins", sa.Column("visitor_mobile", sa.String(length=20), nullable=True))
    op.create_index(op.f("ix_checkins_channel"), "checkins", ["channel"], unique=False)
    op.create_index(op.f("ix_checkins_is_visitor"), "checkins", ["is_visitor"], unique=False)
    op.create_index(op.f("ix_checkins_visitor_mobile"), "checkins", ["visitor_mobile"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_checkins_visitor_mobile"), table_name="checkins")
    op.drop_index(op.f("ix_checkins_is_visitor"), table_name="checkins")
    op.drop_index(op.f("ix_checkins_channel"), table_name="checkins")
    op.drop_column("checkins", "visitor_mobile")
    op.drop_column("checkins", "visitor_name")
    op.drop_column("checkins", "is_visitor")
    op.drop_column("checkins", "channel")
    op.alter_column("checkins", "member_id", existing_type=sa.Integer(), nullable=False)

    op.drop_column("member_profiles", "id_card_back_url")
    op.drop_column("member_profiles", "id_card_front_url")

    op.drop_index(op.f("ix_members_id_card_no"), table_name="members")
    op.drop_index(op.f("ix_members_member_type"), table_name="members")
    op.drop_column("members", "tags")
    op.drop_column("members", "address")
    op.drop_column("members", "wechat")
    op.drop_column("members", "id_card_no")
    op.drop_column("members", "member_type")

from datetime import date
from enum import StrEnum

from sqlalchemy import Boolean, Date, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TimestampMixin


class CardKind(StrEnum):
    TIME = "time"
    TIMES = "times"
    STORED_VALUE = "stored_value"
    PERSONAL_TRAINING = "personal_training"


class CardStatus(StrEnum):
    ACTIVE = "active"
    FROZEN = "frozen"
    EXPIRED = "expired"
    REFUNDED = "refunded"


class CardTransactionType(StrEnum):
    OPEN = "open"
    RENEW = "renew"
    RECHARGE = "recharge"
    CONSUME = "consume"
    FREEZE = "freeze"
    UNFREEZE = "unfreeze"
    REFUND = "refund"
    TRANSFER = "transfer"


class CardType(TimestampMixin, Base):
    __tablename__ = "card_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    kind: Mapped[CardKind] = mapped_column(Enum(CardKind, native_enum=False), index=True)
    price_cents: Mapped[int] = mapped_column(Integer, default=0)
    validity_days: Mapped[int | None] = mapped_column(Integer)
    total_times: Mapped[int | None] = mapped_column(Integer)
    stored_value_cents: Mapped[int | None] = mapped_column(Integer)
    gift_amount_cents: Mapped[int] = mapped_column(Integer, default=0)
    purchase_limit: Mapped[int | None] = mapped_column(Integer)
    applicable_venue_ids: Mapped[str | None] = mapped_column(String(255))
    sale_start_at: Mapped[date | None] = mapped_column(Date)
    sale_end_at: Mapped[date | None] = mapped_column(Date)
    package_kind: Mapped[str | None] = mapped_column(String(40), index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    description: Mapped[str | None] = mapped_column(Text)


class MemberCard(TimestampMixin, Base):
    __tablename__ = "member_cards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"), index=True)
    card_type_id: Mapped[int] = mapped_column(ForeignKey("card_types.id"))
    card_no: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    kind: Mapped[CardKind] = mapped_column(Enum(CardKind, native_enum=False), index=True)
    status: Mapped[CardStatus] = mapped_column(
        Enum(CardStatus, native_enum=False), default=CardStatus.ACTIVE, index=True
    )
    start_date: Mapped[date | None] = mapped_column(Date)
    end_date: Mapped[date | None] = mapped_column(Date, index=True)
    remaining_times: Mapped[int | None] = mapped_column(Integer)
    balance_cents: Mapped[int | None] = mapped_column(Integer)
    frozen_from: Mapped[date | None] = mapped_column(Date)
    remark: Mapped[str | None] = mapped_column(Text)


class CardTransaction(TimestampMixin, Base):
    __tablename__ = "card_transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    member_card_id: Mapped[int] = mapped_column(ForeignKey("member_cards.id"), index=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"), index=True)
    order_id: Mapped[int | None] = mapped_column(ForeignKey("orders.id"))
    transaction_type: Mapped[CardTransactionType] = mapped_column(
        Enum(CardTransactionType, native_enum=False), index=True
    )
    amount_cents: Mapped[int] = mapped_column(Integer, default=0)
    times_delta: Mapped[int] = mapped_column(Integer, default=0)
    balance_after_cents: Mapped[int | None] = mapped_column(Integer)
    times_after: Mapped[int | None] = mapped_column(Integer)
    note: Mapped[str | None] = mapped_column(Text)

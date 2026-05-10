from enum import StrEnum

from sqlalchemy import Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TimestampMixin


class OrderStatus(StrEnum):
    PENDING = "pending"
    PAID = "paid"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class PaymentStatus(StrEnum):
    SUCCESS = "success"
    FAILED = "failed"
    REFUNDED = "refunded"


class Order(TimestampMixin, Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_no: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    member_id: Mapped[int | None] = mapped_column(ForeignKey("members.id"), index=True)
    order_type: Mapped[str] = mapped_column(String(50), index=True)
    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus, native_enum=False), default=OrderStatus.PENDING, index=True
    )
    total_amount_cents: Mapped[int] = mapped_column(Integer, default=0)
    paid_amount_cents: Mapped[int] = mapped_column(Integer, default=0)
    handled_by_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    remark: Mapped[str | None] = mapped_column(Text)


class Payment(TimestampMixin, Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), index=True)
    payment_no: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    method: Mapped[str] = mapped_column(String(50), index=True)
    status: Mapped[PaymentStatus] = mapped_column(
        Enum(PaymentStatus, native_enum=False), default=PaymentStatus.SUCCESS, index=True
    )
    amount_cents: Mapped[int] = mapped_column(Integer)
    paid_by_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    note: Mapped[str | None] = mapped_column(Text)


class Refund(TimestampMixin, Base):
    __tablename__ = "refunds"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), index=True)
    payment_id: Mapped[int | None] = mapped_column(ForeignKey("payments.id"))
    refund_no: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    amount_cents: Mapped[int] = mapped_column(Integer)
    reason: Mapped[str | None] = mapped_column(Text)
    handled_by_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))

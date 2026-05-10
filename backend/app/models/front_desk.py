from datetime import datetime
from enum import StrEnum

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TimestampMixin


class CheckinStatus(StrEnum):
    ACTIVE = "active"
    CHECKED_OUT = "checked_out"


class CheckinChannel(StrEnum):
    CARD = "card"
    QRCODE = "qrcode"
    FACE = "face"
    VISITOR = "visitor"


class BraceletStatus(StrEnum):
    BORROWED = "borrowed"
    RETURNED = "returned"


class Checkin(TimestampMixin, Base):
    __tablename__ = "checkins"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    member_id: Mapped[int | None] = mapped_column(ForeignKey("members.id"), index=True)
    member_card_id: Mapped[int | None] = mapped_column(ForeignKey("member_cards.id"))
    channel: Mapped[CheckinChannel] = mapped_column(
        Enum(CheckinChannel, native_enum=False), default=CheckinChannel.CARD, index=True
    )
    is_visitor: Mapped[bool] = mapped_column(default=False, index=True)
    visitor_name: Mapped[str | None] = mapped_column(String(80))
    visitor_mobile: Mapped[str | None] = mapped_column(String(20), index=True)
    checkin_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    checkout_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    status: Mapped[CheckinStatus] = mapped_column(
        Enum(CheckinStatus, native_enum=False), default=CheckinStatus.ACTIVE, index=True
    )
    bracelet_no: Mapped[str | None] = mapped_column(String(50), index=True)
    handled_by_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))


class BraceletRecord(TimestampMixin, Base):
    __tablename__ = "bracelet_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"), index=True)
    bracelet_no: Mapped[str] = mapped_column(String(50), index=True)
    borrowed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    returned_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    status: Mapped[BraceletStatus] = mapped_column(
        Enum(BraceletStatus, native_enum=False), default=BraceletStatus.BORROWED, index=True
    )
    handled_by_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))

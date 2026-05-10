from datetime import datetime
from enum import StrEnum

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TimestampMixin


class PersonalTrainingSessionStatus(StrEnum):
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


class PersonalTrainingPackage(TimestampMixin, Base):
    __tablename__ = "personal_training_packages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"), index=True)
    coach_id: Mapped[int | None] = mapped_column(ForeignKey("coaches.id"))
    order_id: Mapped[int | None] = mapped_column(ForeignKey("orders.id"))
    name: Mapped[str] = mapped_column(String(120))
    total_sessions: Mapped[int] = mapped_column(Integer)
    remaining_sessions: Mapped[int] = mapped_column(Integer)
    amount_cents: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(30), default="active", index=True)


class PersonalTrainingSession(TimestampMixin, Base):
    __tablename__ = "personal_training_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    package_id: Mapped[int] = mapped_column(ForeignKey("personal_training_packages.id"), index=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"), index=True)
    coach_id: Mapped[int] = mapped_column(ForeignKey("coaches.id"), index=True)
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    status: Mapped[PersonalTrainingSessionStatus] = mapped_column(
        Enum(PersonalTrainingSessionStatus, native_enum=False),
        default=PersonalTrainingSessionStatus.SCHEDULED,
        index=True,
    )
    confirmed_by_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    training_record_id: Mapped[int | None] = mapped_column(ForeignKey("training_records.id"))
    note: Mapped[str | None] = mapped_column(Text)

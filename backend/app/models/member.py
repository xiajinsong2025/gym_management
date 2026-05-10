from enum import StrEnum

from sqlalchemy import Date, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TimestampMixin


class MemberStatus(StrEnum):
    NORMAL = "normal"
    FROZEN = "frozen"
    EXPIRED = "expired"
    LOST = "lost"
    LEAD = "lead"


class Gender(StrEnum):
    UNKNOWN = "unknown"
    MALE = "male"
    FEMALE = "female"


class MemberType(StrEnum):
    REGULAR = "regular"
    YEAR = "year"
    SEASON = "season"
    MONTH = "month"
    TIMES = "times"
    STORED_VALUE = "stored_value"
    VIP = "vip"


class Member(TimestampMixin, Base):
    __tablename__ = "members"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(80), index=True)
    mobile: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    member_no: Mapped[str | None] = mapped_column(String(40), unique=True, index=True)
    gender: Mapped[Gender] = mapped_column(Enum(Gender, native_enum=False), default=Gender.UNKNOWN)
    birthday: Mapped[Date | None] = mapped_column(Date)
    member_type: Mapped[MemberType] = mapped_column(
        Enum(MemberType, native_enum=False), default=MemberType.REGULAR, index=True
    )
    id_card_no: Mapped[str | None] = mapped_column(String(32), index=True)
    wechat: Mapped[str | None] = mapped_column(String(80))
    address: Mapped[str | None] = mapped_column(String(255))
    tags: Mapped[str | None] = mapped_column(Text)
    status: Mapped[MemberStatus] = mapped_column(
        Enum(MemberStatus, native_enum=False), default=MemberStatus.NORMAL, index=True
    )
    source: Mapped[str | None] = mapped_column(String(80))
    consultant_id: Mapped[int | None] = mapped_column(ForeignKey("staff.id"))
    coach_id: Mapped[int | None] = mapped_column(ForeignKey("coaches.id"))
    remark: Mapped[str | None] = mapped_column(Text)


class MemberProfile(TimestampMixin, Base):
    __tablename__ = "member_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id", ondelete="CASCADE"), unique=True)
    avatar_url: Mapped[str | None] = mapped_column(String(255))
    id_card_front_url: Mapped[str | None] = mapped_column(String(255))
    id_card_back_url: Mapped[str | None] = mapped_column(String(255))
    emergency_contact: Mapped[str | None] = mapped_column(String(80))
    emergency_phone: Mapped[str | None] = mapped_column(String(20))
    height_cm: Mapped[int | None] = mapped_column(Integer)
    weight_kg: Mapped[int | None] = mapped_column(Integer)
    fitness_goal: Mapped[str | None] = mapped_column(String(255))


class MemberFollowup(TimestampMixin, Base):
    __tablename__ = "member_followups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id", ondelete="CASCADE"), index=True)
    staff_id: Mapped[int | None] = mapped_column(ForeignKey("staff.id"))
    content: Mapped[str] = mapped_column(Text)
    next_followup_date: Mapped[Date | None] = mapped_column(Date)


class MemberFeedback(TimestampMixin, Base):
    __tablename__ = "member_feedback"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id", ondelete="CASCADE"), index=True)
    category: Mapped[str | None] = mapped_column(String(80))
    content: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(30), default="open", index=True)
    handled_by_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    reply: Mapped[str | None] = mapped_column(Text)


class TrainingRecord(TimestampMixin, Base):
    __tablename__ = "training_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id", ondelete="CASCADE"), index=True)
    coach_id: Mapped[int | None] = mapped_column(ForeignKey("coaches.id"))
    record_date: Mapped[Date] = mapped_column(Date, index=True)
    content: Mapped[str] = mapped_column(Text)
    body_data: Mapped[str | None] = mapped_column(Text)

from datetime import datetime
from enum import StrEnum

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TimestampMixin


class ScheduleStatus(StrEnum):
    SCHEDULED = "scheduled"
    CANCELLED = "cancelled"
    FINISHED = "finished"


class BookingStatus(StrEnum):
    BOOKED = "booked"
    CANCELLED = "cancelled"
    ATTENDED = "attended"
    WAITLISTED = "waitlisted"


class CourseCategory(TimestampMixin, Base):
    __tablename__ = "course_categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text)


class Course(TimestampMixin, Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_id: Mapped[int | None] = mapped_column(ForeignKey("course_categories.id"))
    name: Mapped[str] = mapped_column(String(120), index=True)
    default_capacity: Mapped[int] = mapped_column(Integer, default=0)
    duration_minutes: Mapped[int] = mapped_column(Integer, default=60)
    description: Mapped[str | None] = mapped_column(Text)


class CourseSchedule(TimestampMixin, Base):
    __tablename__ = "course_schedules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), index=True)
    coach_id: Mapped[int | None] = mapped_column(ForeignKey("coaches.id"))
    venue_id: Mapped[int | None] = mapped_column(ForeignKey("venues.id"))
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    capacity: Mapped[int] = mapped_column(Integer, default=0)
    booked_count: Mapped[int] = mapped_column(Integer, default=0)
    waitlisted_count: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[ScheduleStatus] = mapped_column(
        Enum(ScheduleStatus, native_enum=False), default=ScheduleStatus.SCHEDULED, index=True
    )


class CourseBooking(TimestampMixin, Base):
    __tablename__ = "course_bookings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    schedule_id: Mapped[int] = mapped_column(ForeignKey("course_schedules.id"), index=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"), index=True)
    member_card_id: Mapped[int | None] = mapped_column(ForeignKey("member_cards.id"))
    status: Mapped[BookingStatus] = mapped_column(
        Enum(BookingStatus, native_enum=False), default=BookingStatus.BOOKED, index=True
    )
    booked_by_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    note: Mapped[str | None] = mapped_column(Text)


class CourseAttendance(TimestampMixin, Base):
    __tablename__ = "course_attendance"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    booking_id: Mapped[int] = mapped_column(ForeignKey("course_bookings.id"), unique=True)
    schedule_id: Mapped[int] = mapped_column(ForeignKey("course_schedules.id"), index=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"), index=True)
    attended_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    handled_by_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))

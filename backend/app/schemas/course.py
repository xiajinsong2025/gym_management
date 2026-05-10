from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.course import BookingStatus, ScheduleStatus


class CourseCategoryCreate(BaseModel):
    name: str
    description: str | None = None


class CourseCategoryUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class CourseCategoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    created_at: datetime
    updated_at: datetime


class CourseCreate(BaseModel):
    category_id: int | None = None
    name: str
    default_capacity: int = 0
    duration_minutes: int = 60
    description: str | None = None


class CourseUpdate(BaseModel):
    category_id: int | None = None
    name: str | None = None
    default_capacity: int | None = None
    duration_minutes: int | None = None
    description: str | None = None


class CourseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    category_id: int | None
    name: str
    default_capacity: int
    duration_minutes: int
    description: str | None
    created_at: datetime
    updated_at: datetime


class CourseScheduleCreate(BaseModel):
    course_id: int
    coach_id: int | None = None
    venue_id: int | None = None
    start_time: datetime
    end_time: datetime
    capacity: int = 0


class CourseScheduleUpdate(BaseModel):
    coach_id: int | None = None
    venue_id: int | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    capacity: int | None = None
    status: ScheduleStatus | None = None


class CourseScheduleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    course_id: int
    coach_id: int | None
    venue_id: int | None
    start_time: datetime
    end_time: datetime
    capacity: int
    booked_count: int
    waitlisted_count: int
    status: ScheduleStatus
    created_at: datetime
    updated_at: datetime


class CourseBookingCreate(BaseModel):
    member_id: int
    member_card_id: int | None = None
    booked_by_id: int | None = None
    note: str | None = None


class CourseBookingUpdate(BaseModel):
    status: BookingStatus | None = None
    note: str | None = None


class CourseBookingRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    schedule_id: int
    member_id: int
    member_card_id: int | None
    status: BookingStatus
    booked_by_id: int | None
    note: str | None
    created_at: datetime
    updated_at: datetime

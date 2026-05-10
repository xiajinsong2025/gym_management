from datetime import date, datetime

from pydantic import BaseModel, ConfigDict

from app.models.member import Gender, MemberStatus


class MemberCreate(BaseModel):
    name: str
    mobile: str
    member_no: str | None = None
    gender: Gender = Gender.UNKNOWN
    birthday: date | None = None
    source: str | None = None
    remark: str | None = None


class MemberRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    mobile: str
    member_no: str | None
    gender: Gender
    birthday: date | None
    status: MemberStatus
    source: str | None
    remark: str | None
    created_at: datetime
    updated_at: datetime


class MemberUpdate(BaseModel):
    name: str | None = None
    mobile: str | None = None
    member_no: str | None = None
    gender: Gender | None = None
    birthday: date | None = None
    status: MemberStatus | None = None
    source: str | None = None
    remark: str | None = None


class MemberProfileUpsert(BaseModel):
    avatar_url: str | None = None
    emergency_contact: str | None = None
    emergency_phone: str | None = None
    height_cm: int | None = None
    weight_kg: int | None = None
    fitness_goal: str | None = None


class MemberProfileRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    member_id: int
    avatar_url: str | None
    emergency_contact: str | None
    emergency_phone: str | None
    height_cm: int | None
    weight_kg: int | None
    fitness_goal: str | None
    created_at: datetime
    updated_at: datetime


class MemberFollowupCreate(BaseModel):
    staff_id: int | None = None
    content: str
    next_followup_date: date | None = None


class MemberFollowupUpdate(BaseModel):
    staff_id: int | None = None
    content: str | None = None
    next_followup_date: date | None = None


class MemberFollowupRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    member_id: int
    staff_id: int | None
    content: str
    next_followup_date: date | None
    created_at: datetime
    updated_at: datetime


class MemberFeedbackCreate(BaseModel):
    category: str | None = None
    content: str
    status: str = "open"
    handled_by_id: int | None = None
    reply: str | None = None


class MemberFeedbackUpdate(BaseModel):
    category: str | None = None
    content: str | None = None
    status: str | None = None
    handled_by_id: int | None = None
    reply: str | None = None


class MemberFeedbackRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    member_id: int
    category: str | None
    content: str
    status: str
    handled_by_id: int | None
    reply: str | None
    created_at: datetime
    updated_at: datetime


class TrainingRecordCreate(BaseModel):
    coach_id: int | None = None
    record_date: date
    content: str
    body_data: str | None = None


class TrainingRecordUpdate(BaseModel):
    coach_id: int | None = None
    record_date: date | None = None
    content: str | None = None
    body_data: str | None = None


class TrainingRecordRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    member_id: int
    coach_id: int | None
    record_date: date
    content: str
    body_data: str | None
    created_at: datetime
    updated_at: datetime

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.personal_training import PersonalTrainingSessionStatus


class PersonalTrainingPackageCreate(BaseModel):
    member_id: int
    coach_id: int | None = None
    order_id: int | None = None
    name: str
    total_sessions: int
    remaining_sessions: int
    amount_cents: int = 0
    status: str = "active"


class PersonalTrainingPackageUpdate(BaseModel):
    coach_id: int | None = None
    name: str | None = None
    total_sessions: int | None = None
    remaining_sessions: int | None = None
    amount_cents: int | None = None
    status: str | None = None


class PersonalTrainingPackageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    member_id: int
    coach_id: int | None
    order_id: int | None
    name: str
    total_sessions: int
    remaining_sessions: int
    amount_cents: int
    status: str
    created_at: datetime
    updated_at: datetime


class PersonalTrainingSessionCreate(BaseModel):
    package_id: int
    member_id: int
    coach_id: int
    start_time: datetime
    end_time: datetime
    note: str | None = None


class PersonalTrainingSessionUpdate(BaseModel):
    start_time: datetime | None = None
    end_time: datetime | None = None
    status: PersonalTrainingSessionStatus | None = None
    confirmed_by_id: int | None = None
    training_record_id: int | None = None
    note: str | None = None


class PersonalTrainingSessionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    package_id: int
    member_id: int
    coach_id: int
    start_time: datetime
    end_time: datetime
    status: PersonalTrainingSessionStatus
    confirmed_by_id: int | None
    training_record_id: int | None
    note: str | None
    created_at: datetime
    updated_at: datetime

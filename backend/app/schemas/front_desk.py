from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.front_desk import BraceletStatus, CheckinStatus


class CheckinCreate(BaseModel):
    member_id: int
    member_card_id: int | None = None
    bracelet_no: str | None = None
    handled_by_id: int | None = None


class CheckoutRequest(BaseModel):
    handled_by_id: int | None = None


class CheckinRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    member_id: int
    member_card_id: int | None
    checkin_time: datetime
    checkout_time: datetime | None
    status: CheckinStatus
    bracelet_no: str | None
    handled_by_id: int | None
    created_at: datetime
    updated_at: datetime


class BraceletBorrowCreate(BaseModel):
    member_id: int
    bracelet_no: str
    handled_by_id: int | None = None


class BraceletReturnRequest(BaseModel):
    handled_by_id: int | None = None


class BraceletRecordRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    member_id: int
    bracelet_no: str
    borrowed_at: datetime
    returned_at: datetime | None
    status: BraceletStatus
    handled_by_id: int | None
    created_at: datetime
    updated_at: datetime

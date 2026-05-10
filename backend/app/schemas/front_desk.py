from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.front_desk import BraceletStatus, CheckinChannel, CheckinStatus


class CheckinCreate(BaseModel):
    member_id: int | None = None
    member_card_id: int | None = None
    channel: CheckinChannel = CheckinChannel.CARD
    is_visitor: bool = False
    visitor_name: str | None = None
    visitor_mobile: str | None = None
    bracelet_no: str | None = None
    handled_by_id: int | None = None


class CheckoutRequest(BaseModel):
    handled_by_id: int | None = None


class CheckinRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    member_id: int | None
    member_card_id: int | None
    channel: CheckinChannel
    is_visitor: bool
    visitor_name: str | None
    visitor_mobile: str | None
    checkin_time: datetime
    checkout_time: datetime | None
    status: CheckinStatus
    bracelet_no: str | None
    handled_by_id: int | None
    created_at: datetime
    updated_at: datetime


class FrontDeskRealtimeStats(BaseModel):
    in_venue_count: int
    today_checkins: int
    active_member_checkins: int
    active_visitor_checkins: int


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

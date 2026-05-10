from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.marketing import CampaignStatus


class MarketingCampaignCreate(BaseModel):
    title: str
    status: CampaignStatus = CampaignStatus.DRAFT
    start_time: datetime | None = None
    end_time: datetime | None = None
    content: str | None = None


class MarketingCampaignUpdate(BaseModel):
    title: str | None = None
    status: CampaignStatus | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    content: str | None = None


class MarketingCampaignRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    status: CampaignStatus
    start_time: datetime | None
    end_time: datetime | None
    content: str | None
    created_at: datetime
    updated_at: datetime


class CampaignRegistrationCreate(BaseModel):
    member_id: int | None = None
    name: str
    mobile: str
    note: str | None = None


class CampaignRegistrationUpdate(BaseModel):
    member_id: int | None = None
    name: str | None = None
    mobile: str | None = None
    note: str | None = None


class CampaignRegistrationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    campaign_id: int
    member_id: int | None
    name: str
    mobile: str
    note: str | None
    created_at: datetime
    updated_at: datetime


class NotificationCreate(BaseModel):
    title: str
    content: str
    target_type: str = "all"
    published_by_id: int | None = None
    published_at: datetime | None = None


class NotificationUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    target_type: str | None = None
    published_by_id: int | None = None
    published_at: datetime | None = None


class NotificationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    target_type: str
    published_by_id: int | None
    published_at: datetime | None
    created_at: datetime
    updated_at: datetime

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.v1.deps import require_permission
from app.core.database import get_db
from app.core.errors import AppError
from app.models.marketing import CampaignRegistration, MarketingCampaign, Notification
from app.models.member import Member
from app.schemas.common import ApiResponse, PageResponse
from app.schemas.marketing import (
    CampaignRegistrationCreate,
    CampaignRegistrationRead,
    CampaignRegistrationUpdate,
    MarketingCampaignCreate,
    MarketingCampaignRead,
    MarketingCampaignUpdate,
    NotificationCreate,
    NotificationRead,
    NotificationUpdate,
)

router = APIRouter(tags=["marketing"])


@router.post("/marketing/campaigns", response_model=ApiResponse[MarketingCampaignRead])
def create_campaign(
    payload: MarketingCampaignCreate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("marketing:write")),
) -> ApiResponse[MarketingCampaignRead]:
    campaign = MarketingCampaign(**payload.model_dump())
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return ApiResponse(data=MarketingCampaignRead.model_validate(campaign))


@router.get("/marketing/campaigns", response_model=ApiResponse[PageResponse[MarketingCampaignRead]])
def list_campaigns(
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("marketing:read")),
) -> ApiResponse[PageResponse[MarketingCampaignRead]]:
    total = db.scalar(select(func.count()).select_from(MarketingCampaign))
    records = db.scalars(
        select(MarketingCampaign)
        .order_by(MarketingCampaign.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    ).all()
    items = [MarketingCampaignRead.model_validate(it) for it in records]
    return ApiResponse(data=PageResponse(items=items, total=total or 0, page=page, page_size=page_size))


@router.patch("/marketing/campaigns/{campaign_id}", response_model=ApiResponse[MarketingCampaignRead])
def update_campaign(
    campaign_id: int,
    payload: MarketingCampaignUpdate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("marketing:write")),
) -> ApiResponse[MarketingCampaignRead]:
    campaign = db.get(MarketingCampaign, campaign_id)
    if campaign is None:
        raise AppError("campaign not found", code=40461, status_code=404)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(campaign, key, value)
    db.commit()
    db.refresh(campaign)
    return ApiResponse(data=MarketingCampaignRead.model_validate(campaign))


@router.post("/marketing/campaigns/{campaign_id}/registrations", response_model=ApiResponse[CampaignRegistrationRead])
def create_registration(
    campaign_id: int,
    payload: CampaignRegistrationCreate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("marketing:write")),
) -> ApiResponse[CampaignRegistrationRead]:
    campaign = db.get(MarketingCampaign, campaign_id)
    if campaign is None:
        raise AppError("campaign not found", code=40461, status_code=404)
    if payload.member_id is not None:
        member = db.get(Member, payload.member_id)
        if member is None:
            raise AppError("member not found", code=40401, status_code=404)

    reg = CampaignRegistration(campaign_id=campaign_id, **payload.model_dump())
    db.add(reg)
    db.commit()
    db.refresh(reg)
    return ApiResponse(data=CampaignRegistrationRead.model_validate(reg))


@router.get("/marketing/campaigns/{campaign_id}/registrations", response_model=ApiResponse[PageResponse[CampaignRegistrationRead]])
def list_registrations(
    campaign_id: int,
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("marketing:read")),
) -> ApiResponse[PageResponse[CampaignRegistrationRead]]:
    campaign = db.get(MarketingCampaign, campaign_id)
    if campaign is None:
        raise AppError("campaign not found", code=40461, status_code=404)

    total = db.scalar(
        select(func.count()).select_from(CampaignRegistration).where(CampaignRegistration.campaign_id == campaign_id)
    )
    records = db.scalars(
        select(CampaignRegistration)
        .where(CampaignRegistration.campaign_id == campaign_id)
        .order_by(CampaignRegistration.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    ).all()
    items = [CampaignRegistrationRead.model_validate(it) for it in records]
    return ApiResponse(data=PageResponse(items=items, total=total or 0, page=page, page_size=page_size))


@router.patch("/marketing/registrations/{registration_id}", response_model=ApiResponse[CampaignRegistrationRead])
def update_registration(
    registration_id: int,
    payload: CampaignRegistrationUpdate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("marketing:write")),
) -> ApiResponse[CampaignRegistrationRead]:
    reg = db.get(CampaignRegistration, registration_id)
    if reg is None:
        raise AppError("campaign registration not found", code=40462, status_code=404)
    if payload.member_id is not None:
        member = db.get(Member, payload.member_id)
        if member is None:
            raise AppError("member not found", code=40401, status_code=404)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(reg, key, value)
    db.commit()
    db.refresh(reg)
    return ApiResponse(data=CampaignRegistrationRead.model_validate(reg))


@router.post("/marketing/notifications", response_model=ApiResponse[NotificationRead])
def create_notification(
    payload: NotificationCreate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("marketing:write")),
) -> ApiResponse[NotificationRead]:
    notice = Notification(**payload.model_dump())
    db.add(notice)
    db.commit()
    db.refresh(notice)
    return ApiResponse(data=NotificationRead.model_validate(notice))


@router.get("/marketing/notifications", response_model=ApiResponse[PageResponse[NotificationRead]])
def list_notifications(
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("marketing:read")),
) -> ApiResponse[PageResponse[NotificationRead]]:
    total = db.scalar(select(func.count()).select_from(Notification))
    records = db.scalars(
        select(Notification).order_by(Notification.id.desc()).offset((page - 1) * page_size).limit(page_size)
    ).all()
    items = [NotificationRead.model_validate(it) for it in records]
    return ApiResponse(data=PageResponse(items=items, total=total or 0, page=page, page_size=page_size))


@router.patch("/marketing/notifications/{notification_id}", response_model=ApiResponse[NotificationRead])
def update_notification(
    notification_id: int,
    payload: NotificationUpdate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("marketing:write")),
) -> ApiResponse[NotificationRead]:
    notice = db.get(Notification, notification_id)
    if notice is None:
        raise AppError("notification not found", code=40463, status_code=404)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(notice, key, value)
    db.commit()
    db.refresh(notice)
    return ApiResponse(data=NotificationRead.model_validate(notice))

from datetime import UTC, datetime

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.v1.deps import require_permission
from app.core.database import get_db
from app.core.errors import AppError
from app.models.front_desk import BraceletRecord, BraceletStatus, Checkin, CheckinStatus
from app.models.member import Member
from app.schemas.common import ApiResponse, PageResponse
from app.schemas.front_desk import (
    BraceletBorrowCreate,
    BraceletRecordRead,
    BraceletReturnRequest,
    CheckinCreate,
    CheckinRead,
    CheckoutRequest,
)

router = APIRouter(tags=["front-desk"])


@router.post("/checkins", response_model=ApiResponse[CheckinRead])
def create_checkin(
    payload: CheckinCreate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("frontdesk:write")),
) -> ApiResponse[CheckinRead]:
    member = db.get(Member, payload.member_id)
    if member is None:
        raise AppError("member not found", code=40401, status_code=404)

    active = db.scalar(
        select(Checkin).where(Checkin.member_id == payload.member_id, Checkin.status == CheckinStatus.ACTIVE).limit(1)
    )
    if active is not None:
        raise AppError("member already checked in", code=40051, status_code=400)

    checkin = Checkin(
        **payload.model_dump(),
        checkin_time=datetime.now(UTC),
        status=CheckinStatus.ACTIVE,
    )
    db.add(checkin)
    db.commit()
    db.refresh(checkin)
    return ApiResponse(data=CheckinRead.model_validate(checkin))


@router.post("/checkins/{checkin_id}/checkout", response_model=ApiResponse[CheckinRead])
def checkout(
    checkin_id: int,
    payload: CheckoutRequest,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("frontdesk:write")),
) -> ApiResponse[CheckinRead]:
    checkin = db.get(Checkin, checkin_id)
    if checkin is None:
        raise AppError("checkin not found", code=40451, status_code=404)
    if checkin.status != CheckinStatus.ACTIVE:
        raise AppError("checkin already checked out", code=40052, status_code=400)

    checkin.status = CheckinStatus.CHECKED_OUT
    checkin.checkout_time = datetime.now(UTC)
    checkin.handled_by_id = payload.handled_by_id if payload.handled_by_id is not None else checkin.handled_by_id
    db.commit()
    db.refresh(checkin)
    return ApiResponse(data=CheckinRead.model_validate(checkin))


@router.get("/checkins", response_model=ApiResponse[PageResponse[CheckinRead]])
def list_checkins(
    member_id: int | None = None,
    status: CheckinStatus | None = None,
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("frontdesk:read")),
) -> ApiResponse[PageResponse[CheckinRead]]:
    base = select(Checkin)
    count_q = select(func.count()).select_from(Checkin)
    if member_id is not None:
        base = base.where(Checkin.member_id == member_id)
        count_q = count_q.where(Checkin.member_id == member_id)
    if status is not None:
        base = base.where(Checkin.status == status)
        count_q = count_q.where(Checkin.status == status)
    total = db.scalar(count_q)
    records = db.scalars(
        base.order_by(Checkin.checkin_time.desc()).offset((page - 1) * page_size).limit(page_size)
    ).all()
    items = [CheckinRead.model_validate(it) for it in records]
    return ApiResponse(data=PageResponse(items=items, total=total or 0, page=page, page_size=page_size))


@router.post("/bracelets/borrow", response_model=ApiResponse[BraceletRecordRead])
def borrow_bracelet(
    payload: BraceletBorrowCreate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("frontdesk:write")),
) -> ApiResponse[BraceletRecordRead]:
    member = db.get(Member, payload.member_id)
    if member is None:
        raise AppError("member not found", code=40401, status_code=404)

    borrowed = db.scalar(
        select(BraceletRecord)
        .where(BraceletRecord.bracelet_no == payload.bracelet_no, BraceletRecord.status == BraceletStatus.BORROWED)
        .limit(1)
    )
    if borrowed is not None:
        raise AppError("bracelet already borrowed", code=40053, status_code=400)

    record = BraceletRecord(
        **payload.model_dump(),
        borrowed_at=datetime.now(UTC),
        status=BraceletStatus.BORROWED,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return ApiResponse(data=BraceletRecordRead.model_validate(record))


@router.post("/bracelets/{bracelet_no}/return", response_model=ApiResponse[BraceletRecordRead])
def return_bracelet(
    bracelet_no: str,
    payload: BraceletReturnRequest,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("frontdesk:write")),
) -> ApiResponse[BraceletRecordRead]:
    record = db.scalar(
        select(BraceletRecord)
        .where(BraceletRecord.bracelet_no == bracelet_no, BraceletRecord.status == BraceletStatus.BORROWED)
        .order_by(BraceletRecord.id.desc())
        .limit(1)
    )
    if record is None:
        raise AppError("borrowed bracelet record not found", code=40452, status_code=404)

    record.status = BraceletStatus.RETURNED
    record.returned_at = datetime.now(UTC)
    record.handled_by_id = payload.handled_by_id if payload.handled_by_id is not None else record.handled_by_id
    db.commit()
    db.refresh(record)
    return ApiResponse(data=BraceletRecordRead.model_validate(record))


@router.get("/bracelets/records", response_model=ApiResponse[PageResponse[BraceletRecordRead]])
def list_bracelet_records(
    member_id: int | None = None,
    bracelet_no: str | None = None,
    status: BraceletStatus | None = None,
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("frontdesk:read")),
) -> ApiResponse[PageResponse[BraceletRecordRead]]:
    base = select(BraceletRecord)
    count_q = select(func.count()).select_from(BraceletRecord)
    if member_id is not None:
        base = base.where(BraceletRecord.member_id == member_id)
        count_q = count_q.where(BraceletRecord.member_id == member_id)
    if bracelet_no is not None:
        base = base.where(BraceletRecord.bracelet_no == bracelet_no)
        count_q = count_q.where(BraceletRecord.bracelet_no == bracelet_no)
    if status is not None:
        base = base.where(BraceletRecord.status == status)
        count_q = count_q.where(BraceletRecord.status == status)
    total = db.scalar(count_q)
    records = db.scalars(
        base.order_by(BraceletRecord.borrowed_at.desc()).offset((page - 1) * page_size).limit(page_size)
    ).all()
    items = [BraceletRecordRead.model_validate(it) for it in records]
    return ApiResponse(data=PageResponse(items=items, total=total or 0, page=page, page_size=page_size))

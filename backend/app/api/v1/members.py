from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.v1.deps import require_permission
from app.core.database import get_db
from app.core.errors import AppError
from app.models.card import CardTransaction, MemberCard
from app.models.front_desk import Checkin
from app.models.member import Member, MemberFeedback, MemberFollowup, MemberProfile, TrainingRecord
from app.models.personal_training import PersonalTrainingPackage
from app.schemas.common import ApiResponse, PageResponse
from app.schemas.member import (
    MemberCreate,
    MemberFollowupCreate,
    MemberFollowupRead,
    MemberFollowupUpdate,
    MemberFeedbackCreate,
    MemberFeedbackRead,
    MemberFeedbackUpdate,
    MemberProfileRead,
    MemberProfileUpsert,
    MemberRead,
    MemberUpdate,
    TrainingRecordCreate,
    TrainingRecordRead,
    TrainingRecordUpdate,
)

router = APIRouter(prefix="/members", tags=["members"])


@router.post("", response_model=ApiResponse[MemberRead])
def create_member(
    payload: MemberCreate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("members:write")),
) -> ApiResponse[MemberRead]:
    member = Member(**payload.model_dump())
    db.add(member)
    db.commit()
    db.refresh(member)
    return ApiResponse(data=MemberRead.model_validate(member))


@router.get("", response_model=ApiResponse[PageResponse[MemberRead]])
def list_members(
    keyword: str | None = None,
    status: str | None = None,
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("members:read")),
) -> ApiResponse[PageResponse[MemberRead]]:
    page = max(1, page)
    page_size = max(1, min(page_size, 100))

    base_query = select(Member)
    count_query = select(func.count()).select_from(Member)
    if keyword:
        pattern = f"%{keyword}%"
        base_query = base_query.where((Member.name.ilike(pattern)) | (Member.mobile.ilike(pattern)))
        count_query = count_query.where((Member.name.ilike(pattern)) | (Member.mobile.ilike(pattern)))
    if status:
        base_query = base_query.where(Member.status == status)
        count_query = count_query.where(Member.status == status)

    total = db.scalar(count_query)
    offset = (page - 1) * page_size
    records = db.scalars(base_query.order_by(Member.id.desc()).offset(offset).limit(page_size)).all()

    items = [MemberRead.model_validate(record) for record in records]
    data = PageResponse(items=items, total=total or 0, page=page, page_size=page_size)
    return ApiResponse(data=data)


@router.get("/{member_id}", response_model=ApiResponse[MemberRead])
def get_member(
    member_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("members:read")),
) -> ApiResponse[MemberRead]:
    member = db.get(Member, member_id)
    if member is None:
        raise AppError("member not found", code=40401, status_code=404)
    return ApiResponse(data=MemberRead.model_validate(member))


@router.patch("/{member_id}", response_model=ApiResponse[MemberRead])
def update_member(
    member_id: int,
    payload: MemberUpdate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("members:write")),
) -> ApiResponse[MemberRead]:
    member = db.get(Member, member_id)
    if member is None:
        raise AppError("member not found", code=40401, status_code=404)

    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(member, key, value)

    db.commit()
    db.refresh(member)
    return ApiResponse(data=MemberRead.model_validate(member))


@router.put("/{member_id}/profile", response_model=ApiResponse[MemberProfileRead])
def upsert_member_profile(
    member_id: int,
    payload: MemberProfileUpsert,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("members:write")),
) -> ApiResponse[MemberProfileRead]:
    member = db.get(Member, member_id)
    if member is None:
        raise AppError("member not found", code=40401, status_code=404)

    profile = db.scalar(select(MemberProfile).where(MemberProfile.member_id == member_id))
    if profile is None:
        profile = MemberProfile(member_id=member_id, **payload.model_dump())
        db.add(profile)
    else:
        for key, value in payload.model_dump().items():
            setattr(profile, key, value)
    db.commit()
    db.refresh(profile)
    return ApiResponse(data=MemberProfileRead.model_validate(profile))


@router.get("/{member_id}/profile", response_model=ApiResponse[MemberProfileRead])
def get_member_profile(
    member_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("members:read")),
) -> ApiResponse[MemberProfileRead]:
    member = db.get(Member, member_id)
    if member is None:
        raise AppError("member not found", code=40401, status_code=404)

    profile = db.scalar(select(MemberProfile).where(MemberProfile.member_id == member_id))
    if profile is None:
        raise AppError("member profile not found", code=40405, status_code=404)
    return ApiResponse(data=MemberProfileRead.model_validate(profile))


@router.post("/{member_id}/followups", response_model=ApiResponse[MemberFollowupRead])
def create_member_followup(
    member_id: int,
    payload: MemberFollowupCreate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("members:write")),
) -> ApiResponse[MemberFollowupRead]:
    member = db.get(Member, member_id)
    if member is None:
        raise AppError("member not found", code=40401, status_code=404)

    followup = MemberFollowup(member_id=member_id, **payload.model_dump())
    db.add(followup)
    db.commit()
    db.refresh(followup)
    return ApiResponse(data=MemberFollowupRead.model_validate(followup))


@router.get("/{member_id}/followups", response_model=ApiResponse[PageResponse[MemberFollowupRead]])
def list_member_followups(
    member_id: int,
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("members:read")),
) -> ApiResponse[PageResponse[MemberFollowupRead]]:
    member = db.get(Member, member_id)
    if member is None:
        raise AppError("member not found", code=40401, status_code=404)

    page = max(1, page)
    page_size = max(1, min(page_size, 100))
    total = db.scalar(
        select(func.count()).select_from(MemberFollowup).where(MemberFollowup.member_id == member_id)
    )
    offset = (page - 1) * page_size
    records = db.scalars(
        select(MemberFollowup)
        .where(MemberFollowup.member_id == member_id)
        .order_by(MemberFollowup.id.desc())
        .offset(offset)
        .limit(page_size)
    ).all()
    items = [MemberFollowupRead.model_validate(record) for record in records]
    return ApiResponse(data=PageResponse(items=items, total=total or 0, page=page, page_size=page_size))


@router.patch("/{member_id}/followups/{followup_id}", response_model=ApiResponse[MemberFollowupRead])
def update_member_followup(
    member_id: int,
    followup_id: int,
    payload: MemberFollowupUpdate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("members:write")),
) -> ApiResponse[MemberFollowupRead]:
    member = db.get(Member, member_id)
    if member is None:
        raise AppError("member not found", code=40401, status_code=404)

    followup = db.get(MemberFollowup, followup_id)
    if followup is None or followup.member_id != member_id:
        raise AppError("member followup not found", code=40406, status_code=404)

    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(followup, key, value)

    db.commit()
    db.refresh(followup)
    return ApiResponse(data=MemberFollowupRead.model_validate(followup))


@router.post("/{member_id}/feedback", response_model=ApiResponse[MemberFeedbackRead])
def create_member_feedback(
    member_id: int,
    payload: MemberFeedbackCreate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("members:write")),
) -> ApiResponse[MemberFeedbackRead]:
    member = db.get(Member, member_id)
    if member is None:
        raise AppError("member not found", code=40401, status_code=404)

    feedback = MemberFeedback(member_id=member_id, **payload.model_dump())
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return ApiResponse(data=MemberFeedbackRead.model_validate(feedback))


@router.get("/{member_id}/feedback", response_model=ApiResponse[PageResponse[MemberFeedbackRead]])
def list_member_feedback(
    member_id: int,
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("members:read")),
) -> ApiResponse[PageResponse[MemberFeedbackRead]]:
    member = db.get(Member, member_id)
    if member is None:
        raise AppError("member not found", code=40401, status_code=404)

    page = max(1, page)
    page_size = max(1, min(page_size, 100))
    total = db.scalar(select(func.count()).select_from(MemberFeedback).where(MemberFeedback.member_id == member_id))
    offset = (page - 1) * page_size
    records = db.scalars(
        select(MemberFeedback)
        .where(MemberFeedback.member_id == member_id)
        .order_by(MemberFeedback.id.desc())
        .offset(offset)
        .limit(page_size)
    ).all()
    items = [MemberFeedbackRead.model_validate(record) for record in records]
    return ApiResponse(data=PageResponse(items=items, total=total or 0, page=page, page_size=page_size))


@router.patch("/{member_id}/feedback/{feedback_id}", response_model=ApiResponse[MemberFeedbackRead])
def update_member_feedback(
    member_id: int,
    feedback_id: int,
    payload: MemberFeedbackUpdate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("members:write")),
) -> ApiResponse[MemberFeedbackRead]:
    member = db.get(Member, member_id)
    if member is None:
        raise AppError("member not found", code=40401, status_code=404)

    feedback = db.get(MemberFeedback, feedback_id)
    if feedback is None or feedback.member_id != member_id:
        raise AppError("member feedback not found", code=40407, status_code=404)

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(feedback, key, value)
    db.commit()
    db.refresh(feedback)
    return ApiResponse(data=MemberFeedbackRead.model_validate(feedback))


@router.get("/reminders/expiring", response_model=ApiResponse[list[MemberRead]])
def expiring_members(
    days: int = 7,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("members:read")),
) -> ApiResponse[list[MemberRead]]:
    days = max(1, min(days, 90))
    to_date = datetime.now(UTC).date() + timedelta(days=days)
    member_ids = db.scalars(
        select(MemberCard.member_id).where(MemberCard.end_date.is_not(None), MemberCard.end_date <= to_date)
    ).all()
    if not member_ids:
        return ApiResponse(data=[])
    rows = db.scalars(select(Member).where(Member.id.in_(member_ids)).order_by(Member.id.desc())).all()
    return ApiResponse(data=[MemberRead.model_validate(r) for r in rows])


@router.get("/reminders/birthday", response_model=ApiResponse[list[MemberRead]])
def birthday_members(
    days: int = 7,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("members:read")),
) -> ApiResponse[list[MemberRead]]:
    days = max(1, min(days, 31))
    today = datetime.now(UTC).date()
    target_days = {(today + timedelta(days=i)).strftime("%m-%d") for i in range(days + 1)}
    rows = db.scalars(select(Member).where(Member.birthday.is_not(None))).all()
    hit = [r for r in rows if r.birthday and r.birthday.strftime("%m-%d") in target_days]
    return ApiResponse(data=[MemberRead.model_validate(r) for r in sorted(hit, key=lambda x: x.id, reverse=True)])


@router.get("/reminders/dormant", response_model=ApiResponse[list[MemberRead]])
def dormant_members(
    days: int = 30,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("members:read")),
) -> ApiResponse[list[MemberRead]]:
    days = max(7, min(days, 365))
    cutoff = datetime.now(UTC) - timedelta(days=days)
    active_ids = set(db.scalars(select(Checkin.member_id).where(Checkin.checkin_time >= cutoff, Checkin.member_id.is_not(None))).all())
    rows = db.scalars(select(Member).order_by(Member.id.desc())).all()
    dormant = [r for r in rows if r.id not in active_ids]
    return ApiResponse(data=[MemberRead.model_validate(r) for r in dormant])


@router.get("/{member_id}/timeline", response_model=ApiResponse[dict[str, int]])
def member_timeline_summary(
    member_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("members:read")),
) -> ApiResponse[dict[str, int]]:
    member = db.get(Member, member_id)
    if member is None:
        raise AppError("member not found", code=40401, status_code=404)

    card_count = db.scalar(select(func.count()).select_from(MemberCard).where(MemberCard.member_id == member_id)) or 0
    consume_count = db.scalar(
        select(func.count()).select_from(CardTransaction).where(CardTransaction.member_id == member_id)
    ) or 0
    checkin_count = db.scalar(select(func.count()).select_from(Checkin).where(Checkin.member_id == member_id)) or 0
    pt_purchase_count = db.scalar(
        select(func.count()).select_from(PersonalTrainingPackage).where(PersonalTrainingPackage.member_id == member_id)
    ) or 0
    followup_count = db.scalar(
        select(func.count()).select_from(MemberFollowup).where(MemberFollowup.member_id == member_id)
    ) or 0
    return ApiResponse(
        data={
            "card_records": int(card_count),
            "consume_records": int(consume_count),
            "checkin_records": int(checkin_count),
            "pt_purchase_records": int(pt_purchase_count),
            "followup_records": int(followup_count),
        }
    )


@router.post("/{member_id}/training-records", response_model=ApiResponse[TrainingRecordRead])
def create_training_record(
    member_id: int,
    payload: TrainingRecordCreate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("members:write")),
) -> ApiResponse[TrainingRecordRead]:
    member = db.get(Member, member_id)
    if member is None:
        raise AppError("member not found", code=40401, status_code=404)

    record = TrainingRecord(member_id=member_id, **payload.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return ApiResponse(data=TrainingRecordRead.model_validate(record))


@router.get("/{member_id}/training-records", response_model=ApiResponse[PageResponse[TrainingRecordRead]])
def list_training_records(
    member_id: int,
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("members:read")),
) -> ApiResponse[PageResponse[TrainingRecordRead]]:
    member = db.get(Member, member_id)
    if member is None:
        raise AppError("member not found", code=40401, status_code=404)

    page = max(1, page)
    page_size = max(1, min(page_size, 100))
    total = db.scalar(select(func.count()).select_from(TrainingRecord).where(TrainingRecord.member_id == member_id))
    offset = (page - 1) * page_size
    records = db.scalars(
        select(TrainingRecord)
        .where(TrainingRecord.member_id == member_id)
        .order_by(TrainingRecord.record_date.desc(), TrainingRecord.id.desc())
        .offset(offset)
        .limit(page_size)
    ).all()
    items = [TrainingRecordRead.model_validate(record) for record in records]
    return ApiResponse(data=PageResponse(items=items, total=total or 0, page=page, page_size=page_size))


@router.patch("/{member_id}/training-records/{record_id}", response_model=ApiResponse[TrainingRecordRead])
def update_training_record(
    member_id: int,
    record_id: int,
    payload: TrainingRecordUpdate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("members:write")),
) -> ApiResponse[TrainingRecordRead]:
    member = db.get(Member, member_id)
    if member is None:
        raise AppError("member not found", code=40401, status_code=404)

    record = db.get(TrainingRecord, record_id)
    if record is None or record.member_id != member_id:
        raise AppError("training record not found", code=40408, status_code=404)

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(record, key, value)
    db.commit()
    db.refresh(record)
    return ApiResponse(data=TrainingRecordRead.model_validate(record))

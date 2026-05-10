from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.v1.deps import require_permission
from app.core.database import get_db
from app.core.errors import AppError
from app.models.member import Member
from app.models.personal_training import (
    PersonalTrainingPackage,
    PersonalTrainingSession,
    PersonalTrainingSessionStatus,
)
from app.schemas.common import ApiResponse, PageResponse
from app.schemas.personal_training import (
    PersonalTrainingPackageCreate,
    PersonalTrainingPackageRead,
    PersonalTrainingPackageUpdate,
    PersonalTrainingSessionCreate,
    PersonalTrainingSessionRead,
    PersonalTrainingSessionUpdate,
)

router = APIRouter(tags=["personal-training"])


@router.post("/pt/packages", response_model=ApiResponse[PersonalTrainingPackageRead])
def create_package(
    payload: PersonalTrainingPackageCreate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("pt:write")),
) -> ApiResponse[PersonalTrainingPackageRead]:
    member = db.get(Member, payload.member_id)
    if member is None:
        raise AppError("member not found", code=40401, status_code=404)
    package = PersonalTrainingPackage(**payload.model_dump())
    db.add(package)
    db.commit()
    db.refresh(package)
    return ApiResponse(data=PersonalTrainingPackageRead.model_validate(package))


@router.get("/pt/packages", response_model=ApiResponse[PageResponse[PersonalTrainingPackageRead]])
def list_packages(
    member_id: int | None = None,
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("pt:read")),
) -> ApiResponse[PageResponse[PersonalTrainingPackageRead]]:
    base = select(PersonalTrainingPackage)
    count_q = select(func.count()).select_from(PersonalTrainingPackage)
    if member_id is not None:
        base = base.where(PersonalTrainingPackage.member_id == member_id)
        count_q = count_q.where(PersonalTrainingPackage.member_id == member_id)
    total = db.scalar(count_q)
    records = db.scalars(
        base.order_by(PersonalTrainingPackage.id.desc()).offset((page - 1) * page_size).limit(page_size)
    ).all()
    items = [PersonalTrainingPackageRead.model_validate(it) for it in records]
    return ApiResponse(data=PageResponse(items=items, total=total or 0, page=page, page_size=page_size))


@router.patch("/pt/packages/{package_id}", response_model=ApiResponse[PersonalTrainingPackageRead])
def update_package(
    package_id: int,
    payload: PersonalTrainingPackageUpdate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("pt:write")),
) -> ApiResponse[PersonalTrainingPackageRead]:
    package = db.get(PersonalTrainingPackage, package_id)
    if package is None:
        raise AppError("pt package not found", code=40441, status_code=404)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(package, key, value)
    db.commit()
    db.refresh(package)
    return ApiResponse(data=PersonalTrainingPackageRead.model_validate(package))


@router.post("/pt/sessions", response_model=ApiResponse[PersonalTrainingSessionRead])
def create_session(
    payload: PersonalTrainingSessionCreate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("pt:write")),
) -> ApiResponse[PersonalTrainingSessionRead]:
    package = db.get(PersonalTrainingPackage, payload.package_id)
    if package is None:
        raise AppError("pt package not found", code=40441, status_code=404)
    if package.member_id != payload.member_id:
        raise AppError("member/package mismatch", code=40041, status_code=400)
    if package.status != "active":
        raise AppError("pt package is not active", code=40042, status_code=400)

    session = PersonalTrainingSession(
        **payload.model_dump(),
        status=PersonalTrainingSessionStatus.SCHEDULED,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return ApiResponse(data=PersonalTrainingSessionRead.model_validate(session))


@router.get("/pt/sessions", response_model=ApiResponse[PageResponse[PersonalTrainingSessionRead]])
def list_sessions(
    package_id: int | None = None,
    member_id: int | None = None,
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("pt:read")),
) -> ApiResponse[PageResponse[PersonalTrainingSessionRead]]:
    base = select(PersonalTrainingSession)
    count_q = select(func.count()).select_from(PersonalTrainingSession)
    if package_id is not None:
        base = base.where(PersonalTrainingSession.package_id == package_id)
        count_q = count_q.where(PersonalTrainingSession.package_id == package_id)
    if member_id is not None:
        base = base.where(PersonalTrainingSession.member_id == member_id)
        count_q = count_q.where(PersonalTrainingSession.member_id == member_id)
    total = db.scalar(count_q)
    records = db.scalars(
        base.order_by(PersonalTrainingSession.start_time.desc()).offset((page - 1) * page_size).limit(page_size)
    ).all()
    items = [PersonalTrainingSessionRead.model_validate(it) for it in records]
    return ApiResponse(data=PageResponse(items=items, total=total or 0, page=page, page_size=page_size))


@router.patch("/pt/sessions/{session_id}", response_model=ApiResponse[PersonalTrainingSessionRead])
def update_session(
    session_id: int,
    payload: PersonalTrainingSessionUpdate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("pt:write")),
) -> ApiResponse[PersonalTrainingSessionRead]:
    session = db.get(PersonalTrainingSession, session_id)
    if session is None:
        raise AppError("pt session not found", code=40442, status_code=404)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(session, key, value)
    db.commit()
    db.refresh(session)
    return ApiResponse(data=PersonalTrainingSessionRead.model_validate(session))


@router.post("/pt/sessions/{session_id}/confirm", response_model=ApiResponse[PersonalTrainingSessionRead])
def confirm_session(
    session_id: int,
    confirmed_by_id: int | None = None,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("pt:write")),
) -> ApiResponse[PersonalTrainingSessionRead]:
    session = db.get(PersonalTrainingSession, session_id)
    if session is None:
        raise AppError("pt session not found", code=40442, status_code=404)
    if session.status == PersonalTrainingSessionStatus.CANCELLED:
        raise AppError("cancelled session cannot be confirmed", code=40043, status_code=400)
    session.status = PersonalTrainingSessionStatus.CONFIRMED
    session.confirmed_by_id = confirmed_by_id
    db.commit()
    db.refresh(session)
    return ApiResponse(data=PersonalTrainingSessionRead.model_validate(session))


@router.post("/pt/sessions/{session_id}/consume", response_model=ApiResponse[PersonalTrainingSessionRead])
def consume_session(
    session_id: int,
    training_record_id: int | None = None,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("pt:write")),
) -> ApiResponse[PersonalTrainingSessionRead]:
    session = db.get(PersonalTrainingSession, session_id)
    if session is None:
        raise AppError("pt session not found", code=40442, status_code=404)
    if session.status != PersonalTrainingSessionStatus.CONFIRMED:
        raise AppError("session must be confirmed before consume", code=40044, status_code=400)

    package = db.get(PersonalTrainingPackage, session.package_id)
    if package is None:
        raise AppError("pt package not found", code=40441, status_code=404)
    if package.remaining_sessions <= 0:
        raise AppError("no remaining sessions", code=40045, status_code=400)

    package.remaining_sessions -= 1
    session.training_record_id = training_record_id
    session.status = PersonalTrainingSessionStatus.CANCELLED
    if package.remaining_sessions == 0:
        package.status = "finished"

    db.commit()
    db.refresh(session)
    return ApiResponse(data=PersonalTrainingSessionRead.model_validate(session))

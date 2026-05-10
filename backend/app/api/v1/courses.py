from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.v1.deps import require_permission
from app.core.database import get_db
from app.core.errors import AppError
from app.models.course import (
    BookingStatus,
    Course,
    CourseBooking,
    CourseCategory,
    CourseSchedule,
    ScheduleStatus,
)
from app.models.member import Member
from app.schemas.common import ApiResponse, PageResponse
from app.schemas.course import (
    CourseBookingCreate,
    CourseBookingRead,
    CourseBookingUpdate,
    CourseCategoryCreate,
    CourseCategoryRead,
    CourseCategoryUpdate,
    CourseCreate,
    CourseRead,
    CourseScheduleCreate,
    CourseScheduleRead,
    CourseScheduleUpdate,
    CourseUpdate,
)

router = APIRouter(tags=["courses"])


@router.post("/course-categories", response_model=ApiResponse[CourseCategoryRead])
def create_category(
    payload: CourseCategoryCreate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("courses:write")),
) -> ApiResponse[CourseCategoryRead]:
    category = CourseCategory(**payload.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return ApiResponse(data=CourseCategoryRead.model_validate(category))


@router.get("/course-categories", response_model=ApiResponse[PageResponse[CourseCategoryRead]])
def list_categories(
    page: int = 1, page_size: int = 20, db: Session = Depends(get_db), _: object = Depends(require_permission("courses:read"))
) -> ApiResponse[PageResponse[CourseCategoryRead]]:
    total = db.scalar(select(func.count()).select_from(CourseCategory))
    records = db.scalars(
        select(CourseCategory).order_by(CourseCategory.id.desc()).offset((page - 1) * page_size).limit(page_size)
    ).all()
    items = [CourseCategoryRead.model_validate(it) for it in records]
    return ApiResponse(data=PageResponse(items=items, total=total or 0, page=page, page_size=page_size))


@router.patch("/course-categories/{category_id}", response_model=ApiResponse[CourseCategoryRead])
def update_category(
    category_id: int,
    payload: CourseCategoryUpdate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("courses:write")),
) -> ApiResponse[CourseCategoryRead]:
    category = db.get(CourseCategory, category_id)
    if category is None:
        raise AppError("course category not found", code=40421, status_code=404)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(category, key, value)
    db.commit()
    db.refresh(category)
    return ApiResponse(data=CourseCategoryRead.model_validate(category))


@router.post("/courses", response_model=ApiResponse[CourseRead])
def create_course(
    payload: CourseCreate, db: Session = Depends(get_db), _: object = Depends(require_permission("courses:write"))
) -> ApiResponse[CourseRead]:
    course = Course(**payload.model_dump())
    db.add(course)
    db.commit()
    db.refresh(course)
    return ApiResponse(data=CourseRead.model_validate(course))


@router.get("/courses", response_model=ApiResponse[PageResponse[CourseRead]])
def list_courses(
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("courses:read")),
) -> ApiResponse[PageResponse[CourseRead]]:
    total = db.scalar(select(func.count()).select_from(Course))
    records = db.scalars(select(Course).order_by(Course.id.desc()).offset((page - 1) * page_size).limit(page_size)).all()
    items = [CourseRead.model_validate(it) for it in records]
    return ApiResponse(data=PageResponse(items=items, total=total or 0, page=page, page_size=page_size))


@router.patch("/courses/{course_id}", response_model=ApiResponse[CourseRead])
def update_course(
    course_id: int,
    payload: CourseUpdate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("courses:write")),
) -> ApiResponse[CourseRead]:
    course = db.get(Course, course_id)
    if course is None:
        raise AppError("course not found", code=40422, status_code=404)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(course, key, value)
    db.commit()
    db.refresh(course)
    return ApiResponse(data=CourseRead.model_validate(course))


@router.post("/course-schedules", response_model=ApiResponse[CourseScheduleRead])
def create_schedule(
    payload: CourseScheduleCreate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("courses:write")),
) -> ApiResponse[CourseScheduleRead]:
    course = db.get(Course, payload.course_id)
    if course is None:
        raise AppError("course not found", code=40422, status_code=404)

    schedule = CourseSchedule(
        **payload.model_dump(),
        booked_count=0,
        waitlisted_count=0,
        status=ScheduleStatus.SCHEDULED,
    )
    db.add(schedule)
    db.commit()
    db.refresh(schedule)
    return ApiResponse(data=CourseScheduleRead.model_validate(schedule))


@router.get("/course-schedules", response_model=ApiResponse[PageResponse[CourseScheduleRead]])
def list_schedules(
    course_id: int | None = None,
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("courses:read")),
) -> ApiResponse[PageResponse[CourseScheduleRead]]:
    base = select(CourseSchedule)
    count_q = select(func.count()).select_from(CourseSchedule)
    if course_id is not None:
        base = base.where(CourseSchedule.course_id == course_id)
        count_q = count_q.where(CourseSchedule.course_id == course_id)
    total = db.scalar(count_q)
    records = db.scalars(
        base.order_by(CourseSchedule.start_time.desc()).offset((page - 1) * page_size).limit(page_size)
    ).all()
    items = [CourseScheduleRead.model_validate(it) for it in records]
    return ApiResponse(data=PageResponse(items=items, total=total or 0, page=page, page_size=page_size))


@router.patch("/course-schedules/{schedule_id}", response_model=ApiResponse[CourseScheduleRead])
def update_schedule(
    schedule_id: int,
    payload: CourseScheduleUpdate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("courses:write")),
) -> ApiResponse[CourseScheduleRead]:
    schedule = db.get(CourseSchedule, schedule_id)
    if schedule is None:
        raise AppError("course schedule not found", code=40423, status_code=404)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(schedule, key, value)
    db.commit()
    db.refresh(schedule)
    return ApiResponse(data=CourseScheduleRead.model_validate(schedule))


@router.post("/course-schedules/{schedule_id}/bookings", response_model=ApiResponse[CourseBookingRead])
def create_booking(
    schedule_id: int,
    payload: CourseBookingCreate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("courses:write")),
) -> ApiResponse[CourseBookingRead]:
    schedule = db.get(CourseSchedule, schedule_id)
    if schedule is None:
        raise AppError("course schedule not found", code=40423, status_code=404)
    if schedule.status != ScheduleStatus.SCHEDULED:
        raise AppError("course schedule is not bookable", code=40031, status_code=400)

    member = db.get(Member, payload.member_id)
    if member is None:
        raise AppError("member not found", code=40401, status_code=404)

    status = BookingStatus.BOOKED
    if schedule.capacity > 0 and schedule.booked_count >= schedule.capacity:
        status = BookingStatus.WAITLISTED

    booking = CourseBooking(schedule_id=schedule_id, status=status, **payload.model_dump())
    db.add(booking)
    if status == BookingStatus.BOOKED:
        schedule.booked_count += 1
    else:
        schedule.waitlisted_count += 1
    db.commit()
    db.refresh(booking)
    return ApiResponse(data=CourseBookingRead.model_validate(booking))


@router.get("/course-schedules/{schedule_id}/bookings", response_model=ApiResponse[PageResponse[CourseBookingRead]])
def list_bookings(
    schedule_id: int,
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("courses:read")),
) -> ApiResponse[PageResponse[CourseBookingRead]]:
    schedule = db.get(CourseSchedule, schedule_id)
    if schedule is None:
        raise AppError("course schedule not found", code=40423, status_code=404)
    total = db.scalar(select(func.count()).select_from(CourseBooking).where(CourseBooking.schedule_id == schedule_id))
    records = db.scalars(
        select(CourseBooking)
        .where(CourseBooking.schedule_id == schedule_id)
        .order_by(CourseBooking.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    ).all()
    items = [CourseBookingRead.model_validate(it) for it in records]
    return ApiResponse(data=PageResponse(items=items, total=total or 0, page=page, page_size=page_size))


@router.patch("/course-bookings/{booking_id}", response_model=ApiResponse[CourseBookingRead])
def update_booking(
    booking_id: int,
    payload: CourseBookingUpdate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("courses:write")),
) -> ApiResponse[CourseBookingRead]:
    booking = db.get(CourseBooking, booking_id)
    if booking is None:
        raise AppError("course booking not found", code=40424, status_code=404)

    old_status = booking.status
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(booking, key, value)

    schedule = db.get(CourseSchedule, booking.schedule_id)
    if schedule is not None and old_status != booking.status:
        if old_status == BookingStatus.BOOKED:
            schedule.booked_count = max(0, schedule.booked_count - 1)
        if old_status == BookingStatus.WAITLISTED:
            schedule.waitlisted_count = max(0, schedule.waitlisted_count - 1)
        if booking.status == BookingStatus.BOOKED:
            schedule.booked_count += 1
        if booking.status == BookingStatus.WAITLISTED:
            schedule.waitlisted_count += 1

    db.commit()
    db.refresh(booking)
    return ApiResponse(data=CourseBookingRead.model_validate(booking))

from fastapi import APIRouter, Depends
from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

from app.api.v1.deps import get_current_user
from app.core.database import get_db
from app.core.errors import AppError
from app.core.security import hash_password
from app.models.system import Department, Menu, OperationLog, Permission, Role, User, role_permissions
from app.schemas.common import ApiResponse, PageResponse
from app.schemas.system import (
    DepartmentCreate,
    DepartmentRead,
    DepartmentUpdate,
    MenuCreate,
    MenuRead,
    MenuUpdate,
    OperationLogRead,
    PermissionRead,
    RoleCreate,
    RolePermissionUpdate,
    RoleRead,
    RoleUpdate,
    UserCreate,
    UserRead,
    UserUpdate,
)

router = APIRouter(prefix="/system", tags=["system"])


def _page(page: int, page_size: int) -> tuple[int, int]:
    page = max(1, page)
    page_size = max(1, min(page_size, 100))
    return page, page_size


@router.get("/users", response_model=ApiResponse[PageResponse[UserRead]])
def list_users(
    keyword: str | None = None,
    page: int = 1,
    page_size: int = 20,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ApiResponse[PageResponse[UserRead]]:
    page, page_size = _page(page, page_size)
    base_query = select(User)
    count_query = select(func.count()).select_from(User)
    if keyword:
        pattern = f"%{keyword}%"
        base_query = base_query.where((User.username.ilike(pattern)) | (User.display_name.ilike(pattern)))
        count_query = count_query.where((User.username.ilike(pattern)) | (User.display_name.ilike(pattern)))
    total = db.scalar(count_query) or 0
    rows = db.scalars(base_query.order_by(User.id.desc()).offset((page - 1) * page_size).limit(page_size)).all()
    return ApiResponse(data=PageResponse(items=[UserRead.model_validate(r) for r in rows], total=total, page=page, page_size=page_size))


@router.post("/users", response_model=ApiResponse[UserRead])
def create_user(
    payload: UserCreate,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ApiResponse[UserRead]:
    if db.query(User).filter(User.username == payload.username).first() is not None:
        raise AppError("username already exists", code=40901, status_code=409)
    user = User(
        username=payload.username,
        password_hash=hash_password(payload.password),
        display_name=payload.display_name,
        mobile=payload.mobile,
        email=payload.email,
        is_active=payload.is_active,
        is_superuser=payload.is_superuser,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return ApiResponse(data=UserRead.model_validate(user))


@router.patch("/users/{user_id}", response_model=ApiResponse[UserRead])
def update_user(
    user_id: int,
    payload: UserUpdate,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ApiResponse[UserRead]:
    user = db.get(User, user_id)
    if user is None:
        raise AppError("user not found", code=40411, status_code=404)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return ApiResponse(data=UserRead.model_validate(user))


@router.get("/roles", response_model=ApiResponse[PageResponse[RoleRead]])
def list_roles(
    page: int = 1,
    page_size: int = 20,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ApiResponse[PageResponse[RoleRead]]:
    page, page_size = _page(page, page_size)
    total = db.scalar(select(func.count()).select_from(Role)) or 0
    rows = db.scalars(select(Role).order_by(Role.id.desc()).offset((page - 1) * page_size).limit(page_size)).all()
    return ApiResponse(data=PageResponse(items=[RoleRead.model_validate(r) for r in rows], total=total, page=page, page_size=page_size))


@router.post("/roles", response_model=ApiResponse[RoleRead])
def create_role(payload: RoleCreate, _: User = Depends(get_current_user), db: Session = Depends(get_db)) -> ApiResponse[RoleRead]:
    if db.query(Role).filter((Role.name == payload.name) | (Role.code == payload.code)).first() is not None:
        raise AppError("role already exists", code=40902, status_code=409)
    role = Role(**payload.model_dump())
    db.add(role)
    db.commit()
    db.refresh(role)
    return ApiResponse(data=RoleRead.model_validate(role))


@router.patch("/roles/{role_id}", response_model=ApiResponse[RoleRead])
def update_role(
    role_id: int,
    payload: RoleUpdate,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ApiResponse[RoleRead]:
    role = db.get(Role, role_id)
    if role is None:
        raise AppError("role not found", code=40412, status_code=404)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(role, key, value)
    db.commit()
    db.refresh(role)
    return ApiResponse(data=RoleRead.model_validate(role))


@router.get("/permissions", response_model=ApiResponse[list[PermissionRead]])
def list_permissions(_: User = Depends(get_current_user), db: Session = Depends(get_db)) -> ApiResponse[list[PermissionRead]]:
    rows = db.scalars(select(Permission).order_by(Permission.code.asc())).all()
    return ApiResponse(data=[PermissionRead.model_validate(r) for r in rows])


@router.get("/roles/{role_id}/permissions", response_model=ApiResponse[list[str]])
def get_role_permissions(
    role_id: int,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ApiResponse[list[str]]:
    role = db.get(Role, role_id)
    if role is None:
        raise AppError("role not found", code=40412, status_code=404)
    rows = db.execute(
        select(Permission.code)
        .join(role_permissions, role_permissions.c.permission_id == Permission.id)
        .where(role_permissions.c.role_id == role_id)
        .order_by(Permission.code.asc())
    ).all()
    return ApiResponse(data=[r[0] for r in rows])


@router.put("/roles/{role_id}/permissions", response_model=ApiResponse[list[str]])
def update_role_permissions(
    role_id: int,
    payload: RolePermissionUpdate,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ApiResponse[list[str]]:
    role = db.get(Role, role_id)
    if role is None:
        raise AppError("role not found", code=40412, status_code=404)

    db.execute(delete(role_permissions).where(role_permissions.c.role_id == role_id))

    mapped_codes: list[str] = []
    for code in payload.codes:
        permission = db.query(Permission).filter(Permission.code == code).first()
        if permission is None:
            permission = Permission(name=code, code=code, description=f"auto-created {code}")
            db.add(permission)
            db.flush()
        db.execute(role_permissions.insert().values(role_id=role_id, permission_id=permission.id))
        mapped_codes.append(code)

    db.commit()
    return ApiResponse(data=sorted(set(mapped_codes)))


@router.get("/departments", response_model=ApiResponse[PageResponse[DepartmentRead]])
def list_departments(
    page: int = 1,
    page_size: int = 20,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ApiResponse[PageResponse[DepartmentRead]]:
    page, page_size = _page(page, page_size)
    total = db.scalar(select(func.count()).select_from(Department)) or 0
    rows = db.scalars(
        select(Department).order_by(Department.sort_order.asc(), Department.id.desc()).offset((page - 1) * page_size).limit(page_size)
    ).all()
    return ApiResponse(
        data=PageResponse(items=[DepartmentRead.model_validate(r) for r in rows], total=total, page=page, page_size=page_size)
    )


@router.post("/departments", response_model=ApiResponse[DepartmentRead])
def create_department(
    payload: DepartmentCreate,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ApiResponse[DepartmentRead]:
    if db.query(Department).filter(Department.name == payload.name).first() is not None:
        raise AppError("department already exists", code=40903, status_code=409)
    record = Department(**payload.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return ApiResponse(data=DepartmentRead.model_validate(record))


@router.patch("/departments/{department_id}", response_model=ApiResponse[DepartmentRead])
def update_department(
    department_id: int,
    payload: DepartmentUpdate,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ApiResponse[DepartmentRead]:
    record = db.get(Department, department_id)
    if record is None:
        raise AppError("department not found", code=40413, status_code=404)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(record, key, value)
    db.commit()
    db.refresh(record)
    return ApiResponse(data=DepartmentRead.model_validate(record))


@router.get("/menus", response_model=ApiResponse[PageResponse[MenuRead]])
def list_menus(
    page: int = 1,
    page_size: int = 50,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ApiResponse[PageResponse[MenuRead]]:
    page, page_size = _page(page, page_size)
    total = db.scalar(select(func.count()).select_from(Menu)) or 0
    rows = db.scalars(
        select(Menu).order_by(Menu.sort_order.asc(), Menu.id.desc()).offset((page - 1) * page_size).limit(page_size)
    ).all()
    return ApiResponse(data=PageResponse(items=[MenuRead.model_validate(r) for r in rows], total=total, page=page, page_size=page_size))


@router.post("/menus", response_model=ApiResponse[MenuRead])
def create_menu(payload: MenuCreate, _: User = Depends(get_current_user), db: Session = Depends(get_db)) -> ApiResponse[MenuRead]:
    record = Menu(**payload.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return ApiResponse(data=MenuRead.model_validate(record))


@router.patch("/menus/{menu_id}", response_model=ApiResponse[MenuRead])
def update_menu(
    menu_id: int,
    payload: MenuUpdate,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ApiResponse[MenuRead]:
    record = db.get(Menu, menu_id)
    if record is None:
        raise AppError("menu not found", code=40414, status_code=404)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(record, key, value)
    db.commit()
    db.refresh(record)
    return ApiResponse(data=MenuRead.model_validate(record))


@router.get("/logs/operations", response_model=ApiResponse[PageResponse[OperationLogRead]])
def list_operation_logs(
    page: int = 1,
    page_size: int = 20,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ApiResponse[PageResponse[OperationLogRead]]:
    page, page_size = _page(page, page_size)
    total = db.scalar(select(func.count()).select_from(OperationLog)) or 0
    rows = db.scalars(select(OperationLog).order_by(OperationLog.id.desc()).offset((page - 1) * page_size).limit(page_size)).all()
    return ApiResponse(
        data=PageResponse(items=[OperationLogRead.model_validate(r) for r in rows], total=total, page=page, page_size=page_size)
    )

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.v1.deps import get_current_user
from app.core.database import get_db
from app.core.errors import AppError
from app.core.security import create_access_token, hash_password, verify_password
from app.models.system import Permission, Role, User, role_permissions, user_roles
from app.schemas.auth import (
    CurrentUser,
    GrantPermissionsRequest,
    TokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
)
from app.schemas.common import ApiResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=ApiResponse[CurrentUser])
def register(payload: UserRegisterRequest, db: Session = Depends(get_db)) -> ApiResponse[CurrentUser]:
    exists = db.query(User).filter(User.username == payload.username).first()
    if exists is not None:
        raise AppError("username already exists", code=40901, status_code=409)

    user = User(
        username=payload.username,
        password_hash=hash_password(payload.password),
        display_name=payload.display_name,
        is_active=True,
        is_superuser=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return ApiResponse(data=CurrentUser.model_validate(user))


@router.post("/login", response_model=ApiResponse[TokenResponse])
def login(payload: UserLoginRequest, db: Session = Depends(get_db)) -> ApiResponse[TokenResponse]:
    user = db.query(User).filter(User.username == payload.username).first()
    if user is None or not verify_password(payload.password, user.password_hash):
        raise AppError("invalid username or password", code=40104, status_code=401)
    if not user.is_active:
        raise AppError("user is inactive", code=40103, status_code=403)

    token = create_access_token(subject=user.username)
    return ApiResponse(data=TokenResponse(access_token=token))


@router.post("/me/permissions", response_model=ApiResponse[list[str]])
def grant_my_permissions(
    payload: GrantPermissionsRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ApiResponse[list[str]]:
    role_code = f"user:{user.id}:default"
    role = db.query(Role).filter(Role.code == role_code).first()
    if role is None:
        role = Role(name=role_code, code=role_code, description="default self role")
        db.add(role)
        db.flush()

    user_role_exists = db.execute(
        user_roles.select().where(user_roles.c.user_id == user.id, user_roles.c.role_id == role.id)
    ).first()
    if user_role_exists is None:
        db.execute(user_roles.insert().values(user_id=user.id, role_id=role.id))

    granted: list[str] = []
    for code in payload.codes:
        permission = db.query(Permission).filter(Permission.code == code).first()
        if permission is None:
            permission = Permission(name=code, code=code, description=f"auto-created {code}")
            db.add(permission)
            db.flush()

        rp_exists = db.execute(
            role_permissions.select().where(
                role_permissions.c.role_id == role.id, role_permissions.c.permission_id == permission.id
            )
        ).first()
        if rp_exists is None:
            db.execute(role_permissions.insert().values(role_id=role.id, permission_id=permission.id))
        granted.append(code)

    db.commit()
    return ApiResponse(data=granted)


@router.get("/me/permissions", response_model=ApiResponse[list[str]])
def get_my_permissions(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ApiResponse[list[str]]:
    if user.is_superuser:
        codes = db.scalars(select(Permission.code).order_by(Permission.code.asc())).all()
        return ApiResponse(data=list(codes))

    rows = db.execute(
        select(Permission.code)
        .join(role_permissions, role_permissions.c.permission_id == Permission.id)
        .join(user_roles, user_roles.c.role_id == role_permissions.c.role_id)
        .where(user_roles.c.user_id == user.id)
        .order_by(Permission.code.asc())
    ).all()
    return ApiResponse(data=[row[0] for row in rows])

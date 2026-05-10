from fastapi import Depends
from sqlalchemy import select
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.errors import AppError
from app.core.security import decode_access_token
from app.models.system import Permission, User, role_permissions, user_roles

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = decode_access_token(token)
    except ValueError as exc:
        raise AppError("invalid token", code=40101, status_code=401) from exc
    username = payload.get("sub")
    if not username:
        raise AppError("invalid token", code=40101, status_code=401)

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise AppError("user not found", code=40102, status_code=401)
    if not user.is_active:
        raise AppError("user is inactive", code=40103, status_code=403)
    return user


def require_permission(permission_code: str):
    def _checker(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> User:
        if user.is_superuser:
            return user

        query = (
            select(Permission.id)
            .join(role_permissions, role_permissions.c.permission_id == Permission.id)
            .join(user_roles, user_roles.c.role_id == role_permissions.c.role_id)
            .where(user_roles.c.user_id == user.id, Permission.code == permission_code)
            .limit(1)
        )
        permission_id = db.scalar(query)
        if permission_id is None:
            raise AppError("permission denied", code=40301, status_code=403)
        return user

    return _checker

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    display_name: str
    mobile: str | None
    email: str | None
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime


class UserCreate(BaseModel):
    username: str
    password: str
    display_name: str
    mobile: str | None = None
    email: str | None = None
    is_active: bool = True
    is_superuser: bool = False


class UserUpdate(BaseModel):
    display_name: str | None = None
    mobile: str | None = None
    email: str | None = None
    is_active: bool | None = None
    is_superuser: bool | None = None


class RoleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    code: str
    description: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime


class RoleCreate(BaseModel):
    name: str
    code: str
    description: str | None = None
    is_active: bool = True


class RoleUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


class DepartmentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    parent_id: int | None
    sort_order: int
    is_active: bool
    created_at: datetime
    updated_at: datetime


class DepartmentCreate(BaseModel):
    name: str
    parent_id: int | None = None
    sort_order: int = 0
    is_active: bool = True


class DepartmentUpdate(BaseModel):
    name: str | None = None
    parent_id: int | None = None
    sort_order: int | None = None
    is_active: bool | None = None


class MenuRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    parent_id: int | None
    title: str
    path: str
    component: str | None
    icon: str | None
    permission_code: str | None
    sort_order: int
    is_visible: bool
    created_at: datetime
    updated_at: datetime


class MenuCreate(BaseModel):
    parent_id: int | None = None
    title: str
    path: str
    component: str | None = None
    icon: str | None = None
    permission_code: str | None = None
    sort_order: int = 0
    is_visible: bool = True


class MenuUpdate(BaseModel):
    parent_id: int | None = None
    title: str | None = None
    path: str | None = None
    component: str | None = None
    icon: str | None = None
    permission_code: str | None = None
    sort_order: int | None = None
    is_visible: bool | None = None


class OperationLogRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int | None
    action: str
    resource: str | None
    method: str | None
    path: str | None
    ip_address: str | None
    detail: str | None
    created_at: datetime
    updated_at: datetime


class PermissionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    code: str
    description: str | None
    created_at: datetime
    updated_at: datetime


class RolePermissionUpdate(BaseModel):
    codes: list[str]

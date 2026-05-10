from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserRegisterRequest(BaseModel):
    username: str
    password: str
    display_name: str


class UserLoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CurrentUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    display_name: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime


class GrantPermissionsRequest(BaseModel):
    codes: list[str]

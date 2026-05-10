import os
from dataclasses import dataclass
from functools import lru_cache


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "Gym Management System")
    api_v1_prefix: str = os.getenv("API_V1_PREFIX", "/api/v1")
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://postgres:123456@localhost:5432/gym_management",
    )
    secret_key: str = os.getenv("SECRET_KEY", "change-this-in-production")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", str(60 * 8)))


@lru_cache
def get_settings() -> Settings:
    return Settings()

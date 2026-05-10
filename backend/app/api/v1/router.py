from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.courses import router as courses_router
from app.api.v1.front_desk import router as front_desk_router
from app.api.v1.members import router as members_router
from app.api.v1.marketing import router as marketing_router
from app.api.v1.personal_training import router as personal_training_router
from app.api.v1.reports import router as reports_router
from app.api.v1.transactions import router as transactions_router

api_router = APIRouter()


@api_router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


api_router.include_router(members_router)
api_router.include_router(auth_router)
api_router.include_router(transactions_router)
api_router.include_router(courses_router)
api_router.include_router(personal_training_router)
api_router.include_router(front_desk_router)
api_router.include_router(reports_router)
api_router.include_router(marketing_router)

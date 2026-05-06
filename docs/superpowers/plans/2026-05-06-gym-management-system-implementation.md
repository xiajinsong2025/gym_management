# Gym Management System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first runnable single-club gym management system with FastAPI, Vue3, SQLAlchemy, and Alembic.

**Architecture:** Backend is a modular FastAPI application with SQLAlchemy ORM models, service-layer transactions, Alembic migrations, JWT auth, and RBAC dependencies. Frontend is a Vue3 + Vite + TypeScript + Element Plus admin console with dynamic menu routing and API-driven pages.

**Tech Stack:** Python 3.11+, FastAPI, SQLAlchemy 2.x, Alembic, Pydantic v2, Pytest, Vue3, Vite, TypeScript, Pinia, Vue Router, Axios, Element Plus, ECharts.

---

## Scope Note

The design spec covers several business subsystems. This plan implements the first production-shaped version in one repository, but tasks are ordered so each subsystem can be built and verified independently. Mobile UI, multi-club tenancy, WeChat integration, hardware devices, and advanced marketing are excluded.

## File Structure

Create this repository layout:

```text
backend/
  alembic/
  alembic.ini
  app/
    main.py
    api/v1/
      router.py
      auth.py
      system.py
      settings.py
      members.py
      cards.py
      front_desk.py
      courses.py
      personal_training.py
      orders.py
      reports.py
      marketing.py
      mobile.py
    core/
      config.py
      database.py
      security.py
      deps.py
      errors.py
      logging.py
    models/
      base.py
      system.py
      club.py
      member.py
      card.py
      order.py
      front_desk.py
      course.py
      personal_training.py
      marketing.py
    schemas/
      common.py
      auth.py
      system.py
      club.py
      member.py
      card.py
      order.py
      front_desk.py
      course.py
      personal_training.py
      report.py
      marketing.py
    services/
      auth_service.py
      member_service.py
      card_service.py
      checkin_service.py
      course_service.py
      personal_training_service.py
      order_service.py
      report_service.py
    repositories/
      member_repository.py
      report_repository.py
    tests/
      conftest.py
      test_auth.py
      test_member_cards.py
      test_checkins.py
      test_course_bookings.py
      test_personal_training.py
  pyproject.toml
  README.md
frontend/
  index.html
  package.json
  vite.config.ts
  tsconfig.json
  src/
    main.ts
    App.vue
    router/index.ts
    stores/auth.ts
    api/http.ts
    api/modules/
      auth.ts
      members.ts
      cards.ts
      frontDesk.ts
      courses.ts
      personalTraining.ts
      orders.ts
      reports.ts
    layouts/AdminLayout.vue
    views/
      LoginView.vue
      DashboardView.vue
      system/UserListView.vue
      members/MemberListView.vue
      members/LeadListView.vue
      cards/CardTypeListView.vue
      cards/MemberCardListView.vue
      front-desk/CheckinView.vue
      courses/CourseScheduleView.vue
      courses/CourseBookingView.vue
      personal-training/SessionListView.vue
      orders/OrderListView.vue
      finance/ReportView.vue
    styles/main.scss
docs/
  superpowers/
    specs/
    plans/
```

## Task 1: Backend Project Skeleton

**Files:**
- Create: `backend/pyproject.toml`
- Create: `backend/app/main.py`
- Create: `backend/app/api/v1/router.py`
- Create: `backend/app/core/config.py`
- Create: `backend/app/core/database.py`
- Create: `backend/app/core/errors.py`
- Create: `backend/app/models/base.py`
- Create: `backend/app/schemas/common.py`
- Create: `backend/tests/conftest.py`

- [ ] **Step 1: Create backend package and dependencies**

Create `backend/pyproject.toml`:

```toml
[project]
name = "gym-management-backend"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
  "fastapi>=0.110.0",
  "uvicorn[standard]>=0.29.0",
  "sqlalchemy>=2.0.29",
  "alembic>=1.13.1",
  "pydantic-settings>=2.2.1",
  "python-jose[cryptography]>=3.3.0",
  "passlib[bcrypt]>=1.7.4",
  "python-multipart>=0.0.9",
  "email-validator>=2.1.1",
]

[project.optional-dependencies]
dev = [
  "pytest>=8.1.1",
  "pytest-asyncio>=0.23.6",
  "httpx>=0.27.0",
  "ruff>=0.4.1",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]

[tool.ruff]
line-length = 100
target-version = "py311"
```

- [ ] **Step 2: Create config and database core**

Create `backend/app/core/config.py`:

```python
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Gym Management System"
    api_v1_prefix: str = "/api/v1"
    database_url: str = "sqlite+pysqlite:///./gym.db"
    secret_key: str = "change-this-in-production"
    access_token_expire_minutes: int = 60 * 8

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
```

Create `backend/app/core/database.py`:

```python
from collections.abc import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import get_settings


class Base(DeclarativeBase):
    pass


settings = get_settings()
engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

- [ ] **Step 3: Create common schemas and error handling**

Create `backend/app/schemas/common.py`:

```python
from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    code: int = 0
    message: str = "ok"
    data: T | None = None


class PageResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int
```

Create `backend/app/core/errors.py`:

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class AppError(Exception):
    def __init__(self, message: str, code: int = 400):
        self.message = message
        self.code = code


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(status_code=400, content={"code": exc.code, "message": exc.message, "data": None})
```

- [ ] **Step 4: Create FastAPI app and health endpoint**

Create `backend/app/api/v1/router.py`:

```python
from fastapi import APIRouter

api_router = APIRouter()


@api_router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
```

Create `backend/app/main.py`:

```python
from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.errors import register_exception_handlers


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name)
    register_exception_handlers(app)
    app.include_router(api_router, prefix=settings.api_v1_prefix)
    return app


app = create_app()
```

- [ ] **Step 5: Create test client fixture**

Create `backend/tests/conftest.py`:

```python
from fastapi.testclient import TestClient

from app.main import app


def test_client() -> TestClient:
    return TestClient(app)
```

- [ ] **Step 6: Verify backend skeleton**

Run:

```bash
cd backend
python -m pip install -e ".[dev]"
pytest -q
uvicorn app.main:app --reload
```

Expected:

```text
no tests ran
Uvicorn running on http://127.0.0.1:8000
```

## Task 2: Alembic and Core Models

**Files:**
- Create: `backend/alembic.ini`
- Create: `backend/alembic/env.py`
- Create: `backend/app/models/system.py`
- Create: `backend/app/models/club.py`
- Create: `backend/app/models/member.py`
- Create: `backend/app/models/card.py`
- Create: `backend/app/models/order.py`
- Create: `backend/app/models/front_desk.py`
- Create: `backend/app/models/course.py`
- Create: `backend/app/models/personal_training.py`
- Create: `backend/app/models/marketing.py`

- [ ] **Step 1: Define model conventions**

Create `backend/app/models/base.py`:

```python
from datetime import datetime
from sqlalchemy import DateTime, MetaData, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base

naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

Base.metadata = MetaData(naming_convention=naming_convention)


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
```

- [ ] **Step 2: Define system models**

Create `backend/app/models/system.py` with `User`, `Role`, `Permission`, `Menu`, `Department`, `OperationLog`, and `LoginLog`. Include many-to-many association tables `user_roles`, `role_permissions`, and `role_menus`. Required fields: username, password_hash, display_name, is_active, role name, permission code, menu path, menu component, log action, log ip.

- [ ] **Step 3: Define business models**

Create these model files with explicit enums:

```python
class MemberStatus(str, Enum):
    NORMAL = "normal"
    FROZEN = "frozen"
    EXPIRED = "expired"
    LOST = "lost"
    LEAD = "lead"


class CardKind(str, Enum):
    TIME = "time"
    TIMES = "times"
    STORED_VALUE = "stored_value"
    PERSONAL_TRAINING = "personal_training"


class BookingStatus(str, Enum):
    BOOKED = "booked"
    CANCELLED = "cancelled"
    ATTENDED = "attended"
    WAITLISTED = "waitlisted"
```

Required model files:

- `club.py`: `ClubSettings`, `Venue`, `BusinessHour`, `Staff`, `Coach`
- `member.py`: `Member`, `MemberProfile`, `MemberFollowup`, `MemberFeedback`, `TrainingRecord`
- `card.py`: `CardType`, `MemberCard`, `CardTransaction`
- `order.py`: `Order`, `Payment`, `Refund`
- `front_desk.py`: `Checkin`, `BraceletRecord`
- `course.py`: `CourseCategory`, `Course`, `CourseSchedule`, `CourseBooking`, `CourseAttendance`
- `personal_training.py`: `PersonalTrainingPackage`, `PersonalTrainingSession`
- `marketing.py`: `MarketingCampaign`, `CampaignRegistration`, `Notification`

- [ ] **Step 4: Configure Alembic**

Create `backend/alembic/env.py` to import all model modules and use `Base.metadata` as `target_metadata`.

Run:

```bash
cd backend
alembic revision --autogenerate -m "create initial gym schema"
alembic upgrade head
```

Expected:

```text
Running upgrade  -> <revision>, create initial gym schema
```

## Task 3: Auth and RBAC

**Files:**
- Create: `backend/app/core/security.py`
- Create: `backend/app/core/deps.py`
- Create: `backend/app/schemas/auth.py`
- Create: `backend/app/api/v1/auth.py`
- Create: `backend/app/services/auth_service.py`
- Modify: `backend/app/api/v1/router.py`
- Test: `backend/tests/test_auth.py`

- [ ] **Step 1: Write auth API tests**

Create `backend/tests/test_auth.py`:

```python
def test_health_check(test_client):
    response = test_client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

- [ ] **Step 2: Implement password and token helpers**

Create `backend/app/core/security.py`:

```python
from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext

from app.core.config import get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def create_access_token(subject: str) -> str:
    settings = get_settings()
    expires = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    return jwt.encode({"sub": subject, "exp": expires}, settings.secret_key, algorithm="HS256")
```

- [ ] **Step 3: Add login and current-user routes**

Create `backend/app/schemas/auth.py`:

```python
from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CurrentUserResponse(BaseModel):
    id: int
    username: str
    display_name: str
    permissions: list[str]
    menus: list[dict]
```

Implement `/auth/login` and `/auth/me`. Seed a default admin user during development with username `admin` and password `admin123456` in a startup seed function.

- [ ] **Step 4: Verify auth**

Run:

```bash
cd backend
pytest tests/test_auth.py -q
```

Expected:

```text
1 passed
```

## Task 4: Member and Card Domain

**Files:**
- Create: `backend/app/schemas/member.py`
- Create: `backend/app/schemas/card.py`
- Create: `backend/app/services/member_service.py`
- Create: `backend/app/services/card_service.py`
- Create: `backend/app/api/v1/members.py`
- Create: `backend/app/api/v1/cards.py`
- Test: `backend/tests/test_member_cards.py`

- [ ] **Step 1: Write card business tests**

Create tests for:

- creating a member with unique mobile
- rejecting duplicate mobile
- creating a time card order
- generating a member card after paid order
- writing a `card_transactions` row for open-card action

- [ ] **Step 2: Implement member CRUD**

Implement:

- `POST /members`
- `GET /members`
- `GET /members/{member_id}`
- `PUT /members/{member_id}`
- `POST /members/import-preview`

Validation:

- mobile is required and unique
- member status defaults to `normal`
- lead status uses the same `members` table with status `lead`

- [ ] **Step 3: Implement card type and member card APIs**

Implement:

- `POST /card-types`
- `GET /card-types`
- `POST /member-cards/open`
- `POST /member-cards/{card_id}/renew`
- `POST /member-cards/{card_id}/freeze`
- `POST /member-cards/{card_id}/unfreeze`
- `GET /member-cards`

All amount fields use integer cents. Service methods must use a single SQLAlchemy transaction.

- [ ] **Step 4: Verify member and card domain**

Run:

```bash
cd backend
pytest tests/test_member_cards.py -q
```

Expected:

```text
5 passed
```

## Task 5: Front Desk Checkin

**Files:**
- Create: `backend/app/schemas/front_desk.py`
- Create: `backend/app/services/checkin_service.py`
- Create: `backend/app/api/v1/front_desk.py`
- Test: `backend/tests/test_checkins.py`

- [ ] **Step 1: Write checkin tests**

Test cases:

- active member with valid card can check in
- frozen member cannot check in
- expired time card cannot check in
- member can sign out after checkin
- bracelet borrow and return are recorded

- [ ] **Step 2: Implement checkin service**

Implement methods:

```python
class CheckinService:
    def check_in(self, member_id: int, bracelet_no: str | None) -> Checkin:
        """Create an active checkin after validating member status and card availability."""

    def check_out(self, checkin_id: int) -> Checkin:
        """Set checkout time for an active checkin."""

    def borrow_bracelet(self, member_id: int, bracelet_no: str) -> BraceletRecord:
        """Record bracelet borrow and reject duplicate active bracelet numbers."""

    def return_bracelet(self, bracelet_no: str) -> BraceletRecord:
        """Mark the active bracelet borrow record as returned."""
```

- [ ] **Step 3: Implement front desk routes**

Implement:

- `POST /front-desk/checkins`
- `POST /front-desk/checkins/{checkin_id}/checkout`
- `POST /front-desk/bracelets/borrow`
- `POST /front-desk/bracelets/return`
- `GET /front-desk/member-search`

- [ ] **Step 4: Verify checkin flow**

Run:

```bash
cd backend
pytest tests/test_checkins.py -q
```

Expected:

```text
5 passed
```

## Task 6: Course Scheduling and Booking

**Files:**
- Create: `backend/app/schemas/course.py`
- Create: `backend/app/services/course_service.py`
- Create: `backend/app/api/v1/courses.py`
- Create: `backend/app/api/v1/mobile.py`
- Test: `backend/tests/test_course_bookings.py`

- [ ] **Step 1: Write course booking tests**

Test cases:

- create course category and course
- create schedule with coach, venue, capacity, start time, end time
- booking succeeds when capacity is available
- booking becomes waitlisted when capacity is full
- cancelled booking releases capacity
- attendance marks booking as attended

- [ ] **Step 2: Implement course APIs**

Implement:

- `POST /course-categories`
- `POST /courses`
- `GET /courses`
- `POST /course-schedules`
- `GET /course-schedules`
- `POST /course-bookings`
- `POST /course-bookings/{booking_id}/cancel`
- `POST /course-bookings/{booking_id}/attend`

- [ ] **Step 3: Add mobile API aliases**

Expose mobile-reserved routes:

- `GET /mobile/course-schedules`
- `POST /mobile/course-bookings`
- `POST /mobile/course-bookings/{booking_id}/cancel`

These routes reuse the same `CourseService`; no mobile UI is built.

- [ ] **Step 4: Verify course flow**

Run:

```bash
cd backend
pytest tests/test_course_bookings.py -q
```

Expected:

```text
6 passed
```

## Task 7: Personal Training

**Files:**
- Create: `backend/app/schemas/personal_training.py`
- Create: `backend/app/services/personal_training_service.py`
- Create: `backend/app/api/v1/personal_training.py`
- Test: `backend/tests/test_personal_training.py`

- [ ] **Step 1: Write personal training tests**

Test cases:

- create personal training package for member
- schedule a session with coach
- confirm session
- consume one session count after confirmation
- reject consuming when remaining count is zero

- [ ] **Step 2: Implement personal training APIs**

Implement:

- `POST /personal-training/packages`
- `GET /personal-training/packages`
- `POST /personal-training/sessions`
- `GET /personal-training/sessions`
- `POST /personal-training/sessions/{session_id}/confirm`
- `POST /personal-training/sessions/{session_id}/cancel`

- [ ] **Step 3: Verify personal training**

Run:

```bash
cd backend
pytest tests/test_personal_training.py -q
```

Expected:

```text
5 passed
```

## Task 8: Orders, Reports, Logs, and Marketing

**Files:**
- Create: `backend/app/schemas/order.py`
- Create: `backend/app/schemas/report.py`
- Create: `backend/app/schemas/marketing.py`
- Create: `backend/app/services/order_service.py`
- Create: `backend/app/services/report_service.py`
- Create: `backend/app/repositories/report_repository.py`
- Create: `backend/app/api/v1/orders.py`
- Create: `backend/app/api/v1/reports.py`
- Create: `backend/app/api/v1/marketing.py`

- [ ] **Step 1: Implement order and payment read APIs**

Implement:

- `GET /orders`
- `GET /orders/{order_id}`
- `GET /payments`
- `POST /refunds`
- `GET /refunds`

Refund service must write a refund row and a negative financial event without deleting the original payment.

- [ ] **Step 2: Implement dashboard and finance reports**

Implement:

- `GET /reports/dashboard`
- `GET /reports/revenue/daily`
- `GET /reports/revenue/monthly`
- `GET /reports/member-balances`
- `GET /reports/coach-hours`

Report responses use deterministic keys: `date`, `amount_cents`, `count`, `member_id`, `coach_id`, `hours`.

- [ ] **Step 3: Implement marketing campaign APIs**

Implement:

- `POST /marketing/campaigns`
- `GET /marketing/campaigns`
- `PUT /marketing/campaigns/{campaign_id}`
- `POST /marketing/campaigns/{campaign_id}/registrations`
- `GET /marketing/campaigns/{campaign_id}/registrations`

- [ ] **Step 4: Verify all backend tests**

Run:

```bash
cd backend
pytest -q
```

Expected:

```text
all tests pass
```

## Task 9: Frontend Project Skeleton

**Files:**
- Create: `frontend/package.json`
- Create: `frontend/index.html`
- Create: `frontend/vite.config.ts`
- Create: `frontend/tsconfig.json`
- Create: `frontend/src/main.ts`
- Create: `frontend/src/App.vue`
- Create: `frontend/src/router/index.ts`
- Create: `frontend/src/stores/auth.ts`
- Create: `frontend/src/api/http.ts`
- Create: `frontend/src/layouts/AdminLayout.vue`
- Create: `frontend/src/views/LoginView.vue`
- Create: `frontend/src/views/DashboardView.vue`
- Create: `frontend/src/styles/main.scss`

- [ ] **Step 1: Create Vue dependencies**

Create `frontend/package.json`:

```json
{
  "scripts": {
    "dev": "vite --host 127.0.0.1",
    "build": "vue-tsc -b && vite build",
    "preview": "vite preview --host 127.0.0.1"
  },
  "dependencies": {
    "@element-plus/icons-vue": "^2.3.1",
    "axios": "^1.6.8",
    "echarts": "^5.5.0",
    "element-plus": "^2.7.0",
    "pinia": "^2.1.7",
    "vue": "^3.4.21",
    "vue-router": "^4.3.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.0.4",
    "sass": "^1.75.0",
    "typescript": "^5.4.5",
    "vite": "^5.2.8",
    "vue-tsc": "^2.0.11"
  }
}
```

- [ ] **Step 2: Implement app shell**

Create `main.ts`, `App.vue`, router, auth store, Axios client, and `AdminLayout.vue`. The layout includes left menu, top bar, and router view. API base URL is `/api/v1`.

- [ ] **Step 3: Implement login page**

Login form fields:

- username
- password

Submit calls `/auth/login`, stores token, then calls `/auth/me` and redirects to `/dashboard`.

- [ ] **Step 4: Verify frontend skeleton**

Run:

```bash
cd frontend
npm install
npm run build
```

Expected:

```text
✓ built
```

## Task 10: Frontend Business Pages

**Files:**
- Create all page files listed in the file structure.
- Create all API module files listed in the file structure.

- [ ] **Step 1: Implement API modules**

Create one typed Axios wrapper per backend module:

- `auth.ts`
- `members.ts`
- `cards.ts`
- `frontDesk.ts`
- `courses.ts`
- `personalTraining.ts`
- `orders.ts`
- `reports.ts`

Each list method accepts `{ page, page_size, keyword }` and returns backend `PageResponse`.

- [ ] **Step 2: Implement dashboard**

Dashboard calls `/reports/dashboard` and displays:

- today checkins
- today course bookings
- new members
- expiring members
- today revenue
- pending personal training confirmations

- [ ] **Step 3: Implement core CRUD pages**

Implement table, filters, create/edit form, and detail drawer for:

- members
- leads
- card types
- member cards
- course schedules
- course bookings
- personal training sessions
- orders

- [ ] **Step 4: Implement front desk checkin page**

Page flow:

1. Search member by mobile, card number, or name.
2. Display member status and available cards.
3. Click checkin.
4. Optional bracelet number.
5. Show active checkin and checkout action.

- [ ] **Step 5: Implement report page**

Report page has tabs:

- daily revenue
- monthly revenue
- member balances
- coach hours

Use ECharts for daily and monthly revenue charts.

- [ ] **Step 6: Verify frontend**

Run:

```bash
cd frontend
npm run build
```

Expected:

```text
✓ built
```

## Task 11: End-to-End Verification

**Files:**
- Create: `README.md`
- Modify: `backend/README.md`

- [ ] **Step 1: Document local startup**

Create root `README.md` with commands:

```bash
cd backend
python -m pip install -e ".[dev]"
alembic upgrade head
uvicorn app.main:app --reload
```

```bash
cd frontend
npm install
npm run dev
```

- [ ] **Step 2: Run backend verification**

Run:

```bash
cd backend
ruff check .
pytest -q
```

Expected:

```text
All checks passed
all tests pass
```

- [ ] **Step 3: Run frontend verification**

Run:

```bash
cd frontend
npm run build
```

Expected:

```text
✓ built
```

- [ ] **Step 4: Manual smoke test**

Open:

```text
http://127.0.0.1:5173
```

Verify:

- Login with `admin` / `admin123456`.
- Dashboard loads.
- Create member.
- Create card type.
- Open member card.
- Check in member.
- Create course schedule.
- Create course booking.
- Create personal training session.
- Confirm personal training session.
- View finance report.

## Self-Review

Spec coverage:

- System management: covered by Task 3 and frontend auth/menu shell.
- Basic settings: covered by Task 2 models and later CRUD extension through system/settings routes.
- Member management: covered by Task 4 and Task 10.
- Card/order flow: covered by Task 4 and Task 8.
- Front desk: covered by Task 5 and Task 10.
- Course management: covered by Task 6 and Task 10.
- Personal training: covered by Task 7 and Task 10.
- Marketing: covered by Task 8.
- Finance reports: covered by Task 8 and Task 10.
- Mobile API reservation: covered by Task 6.

Known implementation split:

- This plan intentionally implements basic settings CRUD after the core model/migration work, because the first useful business tests depend on member, card, checkin, course, and personal training services.
- Advanced data permissions, hardware, WeChat, mobile UI, and multi-club tenancy remain outside scope as required by the spec.

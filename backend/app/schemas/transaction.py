from datetime import date, datetime

from pydantic import BaseModel, ConfigDict

from app.models.card import CardKind, CardStatus
from app.models.card import CardTransactionType
from app.models.order import OrderStatus, PaymentStatus


class OpenCardRequest(BaseModel):
    member_id: int
    card_type_id: int
    card_no: str
    start_date: date | None = None
    end_date: date | None = None
    remaining_times: int | None = None
    balance_cents: int | None = None
    total_amount_cents: int = 0
    handled_by_id: int | None = None
    remark: str | None = None


class CardTypeCreate(BaseModel):
    name: str
    kind: CardKind
    price_cents: int = 0
    validity_days: int | None = None
    total_times: int | None = None
    stored_value_cents: int | None = None
    gift_amount_cents: int = 0
    purchase_limit: int | None = None
    applicable_venue_ids: str | None = None
    sale_start_at: date | None = None
    sale_end_at: date | None = None
    package_kind: str | None = None
    is_active: bool = True
    description: str | None = None


class CardTypeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    kind: CardKind
    price_cents: int
    validity_days: int | None
    total_times: int | None
    stored_value_cents: int | None
    gift_amount_cents: int
    purchase_limit: int | None
    applicable_venue_ids: str | None
    sale_start_at: date | None
    sale_end_at: date | None
    package_kind: str | None
    is_active: bool
    description: str | None
    created_at: datetime
    updated_at: datetime


class RechargeCardRequest(BaseModel):
    amount_cents: int
    handled_by_id: int | None = None
    remark: str | None = None


class FreezeCardRequest(BaseModel):
    frozen_from: date
    handled_by_id: int | None = None
    remark: str | None = None


class UnfreezeCardRequest(BaseModel):
    handled_by_id: int | None = None
    remark: str | None = None


class MemberCardRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    member_id: int
    card_type_id: int
    card_no: str
    kind: CardKind
    status: CardStatus
    start_date: date | None
    end_date: date | None
    remaining_times: int | None
    balance_cents: int | None
    frozen_from: date | None
    remark: str | None
    created_at: datetime
    updated_at: datetime


class OrderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_no: str
    member_id: int | None
    order_type: str
    status: OrderStatus
    total_amount_cents: int
    paid_amount_cents: int
    handled_by_id: int | None
    remark: str | None
    created_at: datetime
    updated_at: datetime


class CardTransactionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    member_card_id: int
    member_id: int
    order_id: int | None
    transaction_type: CardTransactionType
    amount_cents: int
    times_delta: int
    balance_after_cents: int | None
    times_after: int | None
    note: str | None
    created_at: datetime
    updated_at: datetime


class PaymentCreate(BaseModel):
    order_id: int
    method: str
    amount_cents: int
    paid_by_id: int | None = None
    note: str | None = None


class PaymentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_id: int
    payment_no: str
    method: str
    status: PaymentStatus
    amount_cents: int
    paid_by_id: int | None
    note: str | None
    created_at: datetime
    updated_at: datetime

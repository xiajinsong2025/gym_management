from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.v1.deps import require_permission
from app.core.database import get_db
from app.models.card import CardTransaction, CardType, MemberCard
from app.models.order import Order, Payment
from app.schemas.common import ApiResponse, PageResponse
from app.schemas.transaction import (
    CardTypeCreate,
    CardTypeRead,
    CardTransactionRead,
    FreezeCardRequest,
    MemberCardRead,
    OpenCardRequest,
    OrderRead,
    PaymentCreate,
    PaymentRead,
    RechargeCardRequest,
    UnfreezeCardRequest,
)
from app.services.transaction_service import (
    create_order_payment,
    freeze_member_card,
    open_member_card,
    recharge_member_card,
    unfreeze_member_card,
)

router = APIRouter(tags=["transactions"])


@router.post("/card-types", response_model=ApiResponse[CardTypeRead])
def create_card_type(
    payload: CardTypeCreate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("transactions:write")),
) -> ApiResponse[CardTypeRead]:
    card_type = CardType(**payload.model_dump())
    db.add(card_type)
    db.commit()
    db.refresh(card_type)
    return ApiResponse(data=CardTypeRead.model_validate(card_type))


@router.post("/member-cards/open", response_model=ApiResponse[MemberCardRead])
def open_card(
    payload: OpenCardRequest,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("transactions:write")),
) -> ApiResponse[MemberCardRead]:
    card = open_member_card(db, payload)
    return ApiResponse(data=MemberCardRead.model_validate(card))


@router.post("/member-cards/{card_id}/recharge", response_model=ApiResponse[MemberCardRead])
def recharge_card(
    card_id: int,
    payload: RechargeCardRequest,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("transactions:write")),
) -> ApiResponse[MemberCardRead]:
    card = recharge_member_card(db, card_id, payload)
    return ApiResponse(data=MemberCardRead.model_validate(card))


@router.get("/member-cards", response_model=ApiResponse[PageResponse[MemberCardRead]])
def list_member_cards(
    member_id: int | None = None,
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("transactions:read")),
) -> ApiResponse[PageResponse[MemberCardRead]]:
    page = max(1, page)
    page_size = max(1, min(page_size, 100))

    base_query = select(MemberCard)
    count_query = select(func.count()).select_from(MemberCard)
    if member_id is not None:
        base_query = base_query.where(MemberCard.member_id == member_id)
        count_query = count_query.where(MemberCard.member_id == member_id)

    total = db.scalar(count_query)
    offset = (page - 1) * page_size
    records = db.scalars(base_query.order_by(MemberCard.id.desc()).offset(offset).limit(page_size)).all()
    items = [MemberCardRead.model_validate(record) for record in records]
    data = PageResponse(items=items, total=total or 0, page=page, page_size=page_size)
    return ApiResponse(data=data)


@router.get("/member-cards/{card_id}", response_model=ApiResponse[MemberCardRead])
def get_member_card(
    card_id: int, db: Session = Depends(get_db), _: object = Depends(require_permission("transactions:read"))
) -> ApiResponse[MemberCardRead]:
    card = db.get(MemberCard, card_id)
    if card is None:
        raise HTTPException(status_code=404, detail="member card not found")
    return ApiResponse(data=MemberCardRead.model_validate(card))


@router.post("/member-cards/{card_id}/freeze", response_model=ApiResponse[MemberCardRead])
def freeze_card(
    card_id: int,
    payload: FreezeCardRequest,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("transactions:write")),
) -> ApiResponse[MemberCardRead]:
    card = freeze_member_card(db, card_id, payload)
    return ApiResponse(data=MemberCardRead.model_validate(card))


@router.post("/member-cards/{card_id}/unfreeze", response_model=ApiResponse[MemberCardRead])
def unfreeze_card(
    card_id: int,
    payload: UnfreezeCardRequest,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("transactions:write")),
) -> ApiResponse[MemberCardRead]:
    card = unfreeze_member_card(db, card_id, payload)
    return ApiResponse(data=MemberCardRead.model_validate(card))


@router.get("/member-cards/{card_id}/transactions", response_model=ApiResponse[PageResponse[CardTransactionRead]])
def list_card_transactions(
    card_id: int,
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("transactions:read")),
) -> ApiResponse[PageResponse[CardTransactionRead]]:
    card = db.get(MemberCard, card_id)
    if card is None:
        raise HTTPException(status_code=404, detail="member card not found")

    page = max(1, page)
    page_size = max(1, min(page_size, 100))
    total = db.scalar(
        select(func.count()).select_from(CardTransaction).where(CardTransaction.member_card_id == card_id)
    )
    offset = (page - 1) * page_size
    records = db.scalars(
        select(CardTransaction)
        .where(CardTransaction.member_card_id == card_id)
        .order_by(CardTransaction.id.desc())
        .offset(offset)
        .limit(page_size)
    ).all()
    items = [CardTransactionRead.model_validate(record) for record in records]
    data = PageResponse(items=items, total=total or 0, page=page, page_size=page_size)
    return ApiResponse(data=data)


@router.get("/orders", response_model=ApiResponse[PageResponse[OrderRead]])
def list_orders(
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("transactions:read")),
) -> ApiResponse[PageResponse[OrderRead]]:
    page = max(1, page)
    page_size = max(1, min(page_size, 100))

    total = db.scalar(select(func.count()).select_from(Order))
    offset = (page - 1) * page_size
    records = db.scalars(select(Order).order_by(Order.id.desc()).offset(offset).limit(page_size)).all()
    items = [OrderRead.model_validate(record) for record in records]
    data = PageResponse(items=items, total=total or 0, page=page, page_size=page_size)
    return ApiResponse(data=data)


@router.post("/payments", response_model=ApiResponse[PaymentRead])
def create_payment(
    payload: PaymentCreate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("transactions:write")),
) -> ApiResponse[PaymentRead]:
    payment = create_order_payment(db, payload)
    return ApiResponse(data=PaymentRead.model_validate(payment))


@router.get("/payments", response_model=ApiResponse[PageResponse[PaymentRead]])
def list_payments(
    order_id: int | None = None,
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("transactions:read")),
) -> ApiResponse[PageResponse[PaymentRead]]:
    page = max(1, page)
    page_size = max(1, min(page_size, 100))

    base_query = select(Payment)
    count_query = select(func.count()).select_from(Payment)
    if order_id is not None:
        base_query = base_query.where(Payment.order_id == order_id)
        count_query = count_query.where(Payment.order_id == order_id)

    total = db.scalar(count_query)
    offset = (page - 1) * page_size
    records = db.scalars(base_query.order_by(Payment.id.desc()).offset(offset).limit(page_size)).all()
    items = [PaymentRead.model_validate(record) for record in records]
    data = PageResponse(items=items, total=total or 0, page=page, page_size=page_size)
    return ApiResponse(data=data)

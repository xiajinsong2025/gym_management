from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy.orm import Session

from app.core.errors import AppError
from app.models.card import CardStatus, CardTransaction, CardTransactionType, CardType, MemberCard
from app.models.member import Member
from app.models.order import Order, OrderStatus, Payment, PaymentStatus
from app.schemas.transaction import (
    FreezeCardRequest,
    OpenCardRequest,
    PaymentCreate,
    RechargeCardRequest,
    UnfreezeCardRequest,
)


def _new_no(prefix: str) -> str:
    ts = datetime.now(UTC).strftime("%Y%m%d%H%M%S")
    return f"{prefix}{ts}{uuid4().hex[:6]}"


def open_member_card(db: Session, payload: OpenCardRequest) -> MemberCard:
    member = db.get(Member, payload.member_id)
    if member is None:
        raise AppError("member not found", code=40401, status_code=404)

    card_type = db.get(CardType, payload.card_type_id)
    if card_type is None:
        raise AppError("card type not found", code=40402, status_code=404)

    order = Order(
        order_no=_new_no("ORD"),
        member_id=payload.member_id,
        order_type="open_card",
        status=OrderStatus.PAID,
        total_amount_cents=payload.total_amount_cents,
        paid_amount_cents=payload.total_amount_cents,
        handled_by_id=payload.handled_by_id,
        remark=payload.remark,
    )
    db.add(order)
    db.flush()

    card = MemberCard(
        member_id=payload.member_id,
        card_type_id=payload.card_type_id,
        card_no=payload.card_no,
        kind=card_type.kind,
        status=CardStatus.ACTIVE,
        start_date=payload.start_date,
        end_date=payload.end_date,
        remaining_times=payload.remaining_times,
        balance_cents=payload.balance_cents,
        remark=payload.remark,
    )
    db.add(card)
    db.flush()

    db.add(
        CardTransaction(
            member_card_id=card.id,
            member_id=payload.member_id,
            order_id=order.id,
            transaction_type=CardTransactionType.OPEN,
            amount_cents=payload.total_amount_cents,
            times_delta=payload.remaining_times or 0,
            balance_after_cents=payload.balance_cents,
            times_after=payload.remaining_times,
            note=payload.remark,
        )
    )
    db.commit()
    db.refresh(card)
    return card


def recharge_member_card(db: Session, card_id: int, payload: RechargeCardRequest) -> MemberCard:
    card = db.get(MemberCard, card_id)
    if card is None:
        raise AppError("member card not found", code=40403, status_code=404)

    card.balance_cents = (card.balance_cents or 0) + payload.amount_cents
    order = Order(
        order_no=_new_no("ORD"),
        member_id=card.member_id,
        order_type="card_recharge",
        status=OrderStatus.PAID,
        total_amount_cents=payload.amount_cents,
        paid_amount_cents=payload.amount_cents,
        handled_by_id=payload.handled_by_id,
        remark=payload.remark,
    )
    db.add(order)
    db.flush()

    db.add(
        CardTransaction(
            member_card_id=card.id,
            member_id=card.member_id,
            order_id=order.id,
            transaction_type=CardTransactionType.RECHARGE,
            amount_cents=payload.amount_cents,
            times_delta=0,
            balance_after_cents=card.balance_cents,
            times_after=card.remaining_times,
            note=payload.remark,
        )
    )
    db.commit()
    db.refresh(card)
    return card


def freeze_member_card(db: Session, card_id: int, payload: FreezeCardRequest) -> MemberCard:
    card = db.get(MemberCard, card_id)
    if card is None:
        raise AppError("member card not found", code=40403, status_code=404)

    card.status = CardStatus.FROZEN
    card.frozen_from = payload.frozen_from
    db.add(
        CardTransaction(
            member_card_id=card.id,
            member_id=card.member_id,
            transaction_type=CardTransactionType.FREEZE,
            note=payload.remark,
        )
    )
    db.commit()
    db.refresh(card)
    return card


def unfreeze_member_card(db: Session, card_id: int, payload: UnfreezeCardRequest) -> MemberCard:
    card = db.get(MemberCard, card_id)
    if card is None:
        raise AppError("member card not found", code=40403, status_code=404)

    card.status = CardStatus.ACTIVE
    card.frozen_from = None
    db.add(
        CardTransaction(
            member_card_id=card.id,
            member_id=card.member_id,
            transaction_type=CardTransactionType.UNFREEZE,
            note=payload.remark,
        )
    )
    db.commit()
    db.refresh(card)
    return card


def create_order_payment(db: Session, payload: PaymentCreate) -> Payment:
    order = db.get(Order, payload.order_id)
    if order is None:
        raise AppError("order not found", code=40404, status_code=404)

    payment = Payment(
        order_id=payload.order_id,
        payment_no=_new_no("PAY"),
        method=payload.method,
        status=PaymentStatus.SUCCESS,
        amount_cents=payload.amount_cents,
        paid_by_id=payload.paid_by_id,
        note=payload.note,
    )
    db.add(payment)

    order.paid_amount_cents = (order.paid_amount_cents or 0) + payload.amount_cents
    if order.paid_amount_cents >= order.total_amount_cents:
        order.status = OrderStatus.PAID

    db.commit()
    db.refresh(payment)
    return payment

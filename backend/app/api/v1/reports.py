from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.v1.deps import require_permission
from app.core.database import get_db
from app.models.order import Order, OrderStatus, Payment, PaymentStatus
from app.schemas.common import ApiResponse
from app.schemas.report import RevenueSummaryItem

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/revenue/daily", response_model=ApiResponse[list[RevenueSummaryItem]])
def daily_revenue(
    db: Session = Depends(get_db), _: object = Depends(require_permission("reports:read"))
) -> ApiResponse[list[RevenueSummaryItem]]:
    order_rows = db.execute(
        select(
            func.date(Order.created_at).label("period"),
            func.count(Order.id).label("order_count"),
            func.coalesce(func.sum(Order.paid_amount_cents), 0).label("order_paid_amount_cents"),
        )
        .where(Order.status == OrderStatus.PAID)
        .group_by(func.date(Order.created_at))
        .order_by(func.date(Order.created_at).desc())
    ).all()
    payment_rows = db.execute(
        select(
            func.date(Payment.created_at).label("period"),
            func.coalesce(func.sum(Payment.amount_cents), 0).label("payment_amount_cents"),
        )
        .where(Payment.status == PaymentStatus.SUCCESS)
        .group_by(func.date(Payment.created_at))
    ).all()

    payment_map = {str(row.period): int(row.payment_amount_cents or 0) for row in payment_rows}
    data = [
        RevenueSummaryItem(
            period=str(row.period),
            order_count=int(row.order_count or 0),
            order_paid_amount_cents=int(row.order_paid_amount_cents or 0),
            payment_amount_cents=payment_map.get(str(row.period), 0),
        )
        for row in order_rows
    ]
    return ApiResponse(data=data)


@router.get("/revenue/monthly", response_model=ApiResponse[list[RevenueSummaryItem]])
def monthly_revenue(
    db: Session = Depends(get_db), _: object = Depends(require_permission("reports:read"))
) -> ApiResponse[list[RevenueSummaryItem]]:
    month_expr_order = func.strftime("%Y-%m", Order.created_at)
    month_expr_payment = func.strftime("%Y-%m", Payment.created_at)

    order_rows = db.execute(
        select(
            month_expr_order.label("period"),
            func.count(Order.id).label("order_count"),
            func.coalesce(func.sum(Order.paid_amount_cents), 0).label("order_paid_amount_cents"),
        )
        .where(Order.status == OrderStatus.PAID)
        .group_by(month_expr_order)
        .order_by(month_expr_order.desc())
    ).all()
    payment_rows = db.execute(
        select(
            month_expr_payment.label("period"),
            func.coalesce(func.sum(Payment.amount_cents), 0).label("payment_amount_cents"),
        )
        .where(Payment.status == PaymentStatus.SUCCESS)
        .group_by(month_expr_payment)
    ).all()

    payment_map = {str(row.period): int(row.payment_amount_cents or 0) for row in payment_rows}
    data = [
        RevenueSummaryItem(
            period=str(row.period),
            order_count=int(row.order_count or 0),
            order_paid_amount_cents=int(row.order_paid_amount_cents or 0),
            payment_amount_cents=payment_map.get(str(row.period), 0),
        )
        for row in order_rows
    ]
    return ApiResponse(data=data)

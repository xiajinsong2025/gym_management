from pydantic import BaseModel


class RevenueSummaryItem(BaseModel):
    period: str
    order_count: int
    order_paid_amount_cents: int
    payment_amount_cents: int

from pydantic import BaseModel
from datetime import datetime

class PayoutItemBase(BaseModel):
    worker_id: int
    days_worked: int
    amount: float

class PayoutItemCreate(PayoutItemBase):
    batch_id: int

class PayoutItemOut(PayoutItemBase):
    id: int
    batch_id: int
    mpesa_checkout_id: str | None = None
    mpesa_status: str | None = None
    mpesa_receipt: str | None = None
    created_at: datetime

    class Config:
        orm_mode = True

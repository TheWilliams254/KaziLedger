from pydantic import BaseModel
from datetime import date, datetime
from typing import List
from .payout_item import PayoutItemOut

class PayoutBatchBase(BaseModel):
    subcontractor_id: int
    date_from: date
    date_to: date

class PayoutBatchCreate(PayoutBatchBase):
    pass

class PayoutBatchOut(PayoutBatchBase):
    id: int
    amount_total: float
    status: str
    created_at: datetime
    items: List[PayoutItemOut] | None = None

    class Config:
        orm_mode = True

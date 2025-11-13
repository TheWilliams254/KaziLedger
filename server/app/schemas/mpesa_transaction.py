from pydantic import BaseModel
from datetime import datetime

class MpesaTransactionBase(BaseModel):
    phone: str
    amount: float

class MpesaTransactionCreate(MpesaTransactionBase):
    checkout_request_id: str | None = None
    merchant_request_id: str | None = None

class MpesaTransactionOut(MpesaTransactionBase):
    id: int
    result_code: int | None = None
    receipt_number: str | None = None
    timestamp: datetime
    payload_json: dict | None = None

    class Config:
        orm_mode = True

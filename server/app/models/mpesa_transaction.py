from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from . import Base

class MpesaTransaction(Base):
    __tablename__ = "mpesa_transactions"

    id = Column(Integer, primary_key=True, index=True)
    checkout_request_id = Column(String(100))
    merchant_request_id = Column(String(100))
    phone = Column(String(20), nullable=False)
    amount = Column(Float, nullable=False)
    result_code = Column(Integer)
    receipt_number = Column(String(50))
    timestamp = Column(DateTime, default=datetime.utcnow)
    payload_json = Column(JSON)

    def __repr__(self):
        return f"<MpesaTransaction(phone={self.phone}, amount={self.amount}, code={self.result_code})>"

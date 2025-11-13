from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from . import Base

class PayoutItem(Base):
    __tablename__ = "payout_items"

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("payout_batches.id"), nullable=False)
    worker_id = Column(Integer, ForeignKey("workers.id"), nullable=False)
    days_worked = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    mpesa_checkout_id = Column(String(100))
    mpesa_status = Column(String(30), default="pending")
    mpesa_receipt = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

    batch = relationship("PayoutBatch", back_populates="items")
    worker = relationship("Worker", back_populates="payout_items")

    def __repr__(self):
        return f"<PayoutItem(worker_id={self.worker_id}, amount={self.amount}, status={self.mpesa_status})>"

from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from . import Base

class PayoutBatch(Base):
    __tablename__ = "payout_batches"

    id = Column(Integer, primary_key=True, index=True)
    subcontractor_id = Column(Integer, ForeignKey("subcontractors.id"), nullable=False)
    date_from = Column(Date, nullable=False)
    date_to = Column(Date, nullable=False)
    amount_total = Column(Float, default=0.0)
    status = Column(String(30), default="prepared")
    created_at = Column(DateTime, default=datetime.utcnow)

    subcontractor = relationship("Subcontractor", back_populates="payout_batches")
    items = relationship("PayoutItem", back_populates="batch", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<PayoutBatch(id={self.id}, total={self.amount_total}, status={self.status})>"

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from . import Base

class Worker(Base):
    __tablename__ = "workers"

    id = Column(Integer, primary_key=True, index=True)
    subcontractor_id = Column(Integer, ForeignKey("subcontractors.id"), nullable=False)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    id_no = Column(String(20))
    daily_rate = Column(Float, default=500.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    subcontractor = relationship("Subcontractor", back_populates="workers")
    attendances = relationship("Attendance", back_populates="worker", cascade="all, delete-orphan")
    payout_items = relationship("PayoutItem", back_populates="worker", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Worker(name={self.name}, phone={self.phone})>"

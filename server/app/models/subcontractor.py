from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from . import Base

class Subcontractor(Base):
    __tablename__ = "subcontractors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    workers = relationship("Worker", back_populates="subcontractor", cascade="all, delete-orphan")
    payout_batches = relationship("PayoutBatch", back_populates="subcontractor", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Subcontractor(name={self.name})>"

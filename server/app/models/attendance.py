from datetime import datetime
from sqlalchemy import Column, Integer, Date, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from . import Base

class Attendance(Base):
    __tablename__ = "attendances"

    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(Integer, ForeignKey("workers.id"), nullable=False)
    date = Column(Date, nullable=False)
    present = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    worker = relationship("Worker", back_populates="attendances")

    def __repr__(self):
        return f"<Attendance(worker_id={self.worker_id}, date={self.date}, present={self.present})>"

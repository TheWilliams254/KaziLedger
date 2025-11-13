from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
class AttendanceBase(BaseModel):
    worker_id: int
    date: date
    present: bool

class AttendanceCreate(BaseModel):
    worker_id: int
    present: bool
    date: Optional[date] = None  # optional  # optional


class AttendanceOut(AttendanceBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

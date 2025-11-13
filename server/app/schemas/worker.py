from pydantic import BaseModel
from datetime import datetime

class WorkerBase(BaseModel):
    name: str
    phone: str
    id_no: str | None = None
    daily_rate: float | None = 500.0

class WorkerCreate(WorkerBase):
    subcontractor_id: int

class WorkerOut(WorkerBase):
    id: int
    subcontractor_id: int
    created_at: datetime

    class Config:
        orm_mode = True

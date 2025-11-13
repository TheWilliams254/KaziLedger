from pydantic import BaseModel, EmailStr
from datetime import datetime

class SubcontractorBase(BaseModel):
    name: str
    email: EmailStr
    phone: str

class SubcontractorCreate(SubcontractorBase):
    password: str

class SubcontractorOut(SubcontractorBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

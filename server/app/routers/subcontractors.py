from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Subcontractor
from app.schemas import SubcontractorCreate, SubcontractorOut
from app.database import SessionLocal
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=SubcontractorOut)
def create_subcontractor(sub: SubcontractorCreate, db: Session = Depends(get_db)):
    hashed = pwd_context.hash(sub.password)
    new_sub = Subcontractor(
        name=sub.name, email=sub.email, phone=sub.phone, password_hash=hashed
    )
    db.add(new_sub)
    db.commit()
    db.refresh(new_sub)
    return new_sub

@router.get("/", response_model=list[SubcontractorOut])
def list_subcontractors(db: Session = Depends(get_db)):
    return db.query(Subcontractor).all()

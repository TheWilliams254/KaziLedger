from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Subcontractor
from app.schemas import SubcontractorCreate, SubcontractorOut
from app.core.auth import (
    get_password_hash, verify_password,
    create_access_token, get_current_subcontractor
)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=SubcontractorOut)
def register(sub: SubcontractorCreate, db: Session = Depends(get_db)):
    existing = db.query(Subcontractor).filter(Subcontractor.email == sub.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = get_password_hash(sub.password)
    new_sub = Subcontractor(
        name=sub.name, email=sub.email, phone=sub.phone, password_hash=hashed_pw
    )
    db.add(new_sub)
    db.commit()
    db.refresh(new_sub)
    return new_sub

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    subcontractor = db.query(Subcontractor).filter(Subcontractor.email == form_data.username).first()
    if not subcontractor or not verify_password(form_data.password, subcontractor.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token({"sub_id": subcontractor.id})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=SubcontractorOut)
def get_profile(current_user: Subcontractor = Depends(get_current_subcontractor)):
    return current_user

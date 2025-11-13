from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from typing import List
from pydantic import BaseModel
from app.models import Attendance, Worker
from app.schemas import AttendanceCreate, AttendanceOut
from app.database import SessionLocal
from app.core.auth import get_current_subcontractor

router = APIRouter()

# ---------------------------
# DB dependency
# ---------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------
# Bulk attendance schema
# ---------------------------
class AttendanceBulk(BaseModel):
    records: List[AttendanceCreate]

# ---------------------------
# Record single attendance
# ---------------------------
@router.post("/rollcall", response_model=AttendanceOut)
def record_attendance(
    att: AttendanceCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_subcontractor)
):
    # Default to today if not provided
    att.date = att.date or date.today()

    # Make sure the worker belongs to the logged-in subcontractor
    worker = db.query(Worker).filter(
        Worker.id == att.worker_id,
        Worker.subcontractor_id == current_user.id
    ).first()
    
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found or not yours")

    # Prevent duplicate roll call for the same date
    existing = db.query(Attendance).filter(
        Attendance.worker_id == att.worker_id,
        Attendance.date == att.date
    ).first()
    if existing:
        existing.present = att.present
        db.commit()
        db.refresh(existing)
        return existing

    new_att = Attendance(**att.dict())
    db.add(new_att)
    db.commit()
    db.refresh(new_att)
    return new_att

# ---------------------------
# Bulk roll call
# ---------------------------
@router.post("/rollcall/bulk")
def bulk_rollcall(
    data: AttendanceBulk,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_subcontractor)
):
    results = []
    for att in data.records:
        att.date = att.date or date.today()
        worker = db.query(Worker).filter(
            Worker.id == att.worker_id,
            Worker.subcontractor_id == current_user.id
        ).first()
        if not worker:
            continue  # skip invalid workers

        existing = db.query(Attendance).filter(
            Attendance.worker_id == att.worker_id,
            Attendance.date == att.date
        ).first()

        if existing:
            existing.present = att.present
            db.commit()
            db.refresh(existing)
            results.append(existing)
        else:
            new_att = Attendance(**att.dict())
            db.add(new_att)
            db.commit()
            db.refresh(new_att)
            results.append(new_att)

    return results

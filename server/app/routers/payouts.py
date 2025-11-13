from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from app.models import PayoutBatch, PayoutItem, Attendance, Worker
from app.schemas import PayoutBatchCreate, PayoutBatchOut
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=PayoutBatchOut)
def create_payout_batch(batch_data: PayoutBatchCreate, db: Session = Depends(get_db)):
    subcontractor_id = batch_data.subcontractor_id
    workers = db.query(Worker).filter(Worker.subcontractor_id == subcontractor_id).all()
    if not workers:
        raise HTTPException(status_code=404, detail="No workers found")

    new_batch = PayoutBatch(**batch_data.dict())
    db.add(new_batch)
    db.commit()
    db.refresh(new_batch)

    total = 0
    for worker in workers:
        days_worked = db.query(func.count(Attendance.id)).filter(
            Attendance.worker_id == worker.id,
            Attendance.date.between(batch_data.date_from, batch_data.date_to),
            Attendance.present == True
        ).scalar()

        amount = days_worked * worker.daily_rate
        payout_item = PayoutItem(
            batch_id=new_batch.id,
            worker_id=worker.id,
            days_worked=days_worked,
            amount=amount
        )
        total += amount
        db.add(payout_item)

    new_batch.amount_total = total
    db.commit()
    db.refresh(new_batch)
    return new_batch

@router.get("/", response_model=list[PayoutBatchOut])
def list_batches(db: Session = Depends(get_db)):
    return db.query(PayoutBatch).all()

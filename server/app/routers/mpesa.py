from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import PayoutItem, MpesaTransaction
from app.schemas import MpesaTransactionCreate, MpesaTransactionOut
from app.database import SessionLocal
from datetime import datetime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/simulate", response_model=MpesaTransactionOut)
def simulate_mpesa(txn: MpesaTransactionCreate, db: Session = Depends(get_db)):
    # Placeholder for M-Pesa API integration
    new_txn = MpesaTransaction(
        phone=txn.phone,
        amount=txn.amount,
        checkout_request_id=txn.checkout_request_id,
        merchant_request_id=txn.merchant_request_id,
        result_code=0,
        receipt_number=f"MPESA{int(datetime.utcnow().timestamp())}",
        payload_json={"status": "Simulated Success"}
    )
    db.add(new_txn)
    db.commit()
    db.refresh(new_txn)
    return new_txn

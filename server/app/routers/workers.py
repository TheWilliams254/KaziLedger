from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models import Worker
from app.schemas import WorkerCreate, WorkerOut
from app.database import SessionLocal
from app.core.auth import get_current_subcontractor

router = APIRouter()

# ---------------------------
# Database Dependency
# ---------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------
# Create Worker
# ---------------------------
@router.post("/", response_model=WorkerOut)
def create_worker(
    worker: WorkerCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_subcontractor)
):
    # Only allow subcontractor to add their own workers
    if worker.subcontractor_id != current_user.id:
        raise HTTPException(status_code=403, detail="Cannot add worker for another subcontractor")

    new_worker = Worker(**worker.dict())
    db.add(new_worker)
    db.commit()
    db.refresh(new_worker)
    return new_worker

# ---------------------------
# List Workers
# ---------------------------
@router.get("/", response_model=List[WorkerOut])
def list_workers(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_subcontractor)
):
    return db.query(Worker).filter(Worker.subcontractor_id == current_user.id).all()

# ---------------------------
# Get Worker by ID
# ---------------------------
@router.get("/{worker_id}", response_model=WorkerOut)
def get_worker(
    worker_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_subcontractor)
):
    worker = db.query(Worker).filter(
        Worker.id == worker_id,
        Worker.subcontractor_id == current_user.id
    ).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    return worker

# ---------------------------
# Update Worker
# ---------------------------
@router.put("/{worker_id}", response_model=WorkerOut)
def update_worker(
    worker_id: int,
    worker_data: WorkerCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_subcontractor)
):
    worker = db.query(Worker).filter(
        Worker.id == worker_id,
        Worker.subcontractor_id == current_user.id
    ).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    for key, value in worker_data.dict().items():
        setattr(worker, key, value)
    db.commit()
    db.refresh(worker)
    return worker

# ---------------------------
# Delete Worker
# ---------------------------
@router.delete("/{worker_id}", response_model=dict)
def delete_worker(
    worker_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_subcontractor)
):
    worker = db.query(Worker).filter(
        Worker.id == worker_id,
        Worker.subcontractor_id == current_user.id
    ).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    
    db.delete(worker)
    db.commit()
    return {"detail": "Worker deleted successfully"}

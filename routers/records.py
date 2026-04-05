from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from dependencies import require_admin, require_analyst, require_viewer
from datetime import datetime
from typing import Optional
import models, schemas

router = APIRouter(prefix="/records", tags=["Financial Records"])

# Create a new financial record (Admin only)
@router.post("/", response_model=schemas.RecordOut)
def create_record(
    record: schemas.RecordCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin)
):
    # Validate type
    if record.type not in ["income", "expense"]:
        raise HTTPException(status_code=400, detail="Type must be income or expense")

    new_record = models.FinancialRecord(
        amount=record.amount,
        type=record.type,
        category=record.category,
        date=record.date,
        notes=record.notes,
        created_by=current_user.id
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

# Get all financial records with filters (All roles)
@router.get("/", response_model=list[schemas.RecordOut])
def get_records(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_viewer),
    type: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
):
    query = db.query(models.FinancialRecord).filter(
        models.FinancialRecord.is_deleted == False
    )

    if type:
        query = query.filter(models.FinancialRecord.type == type)
    if category:
        query = query.filter(models.FinancialRecord.category == category)
    if start_date:
        query = query.filter(models.FinancialRecord.date >= start_date)
    if end_date:
        query = query.filter(models.FinancialRecord.date <= end_date)

    return query.all()

# Get a single record by ID (All roles)
@router.get("/{record_id}", response_model=schemas.RecordOut)
def get_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_viewer)
):
    record = db.query(models.FinancialRecord).filter(
        models.FinancialRecord.id == record_id,
        models.FinancialRecord.is_deleted == False
    ).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

# Update a record (Admin only)
@router.put("/{record_id}", response_model=schemas.RecordOut)
def update_record(
    record_id: int,
    updates: schemas.RecordUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin)
):
    record = db.query(models.FinancialRecord).filter(
        models.FinancialRecord.id == record_id,
        models.FinancialRecord.is_deleted == False
    ).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    if updates.amount is not None:
        record.amount = updates.amount
    if updates.type is not None:
        record.type = updates.type
    if updates.category is not None:
        record.category = updates.category
    if updates.date is not None:
        record.date = updates.date
    if updates.notes is not None:
        record.notes = updates.notes

    db.commit()
    db.refresh(record)
    return record

# Soft delete a record (Admin only)
@router.delete("/{record_id}")
def delete_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin)
):
    record = db.query(models.FinancialRecord).filter(
        models.FinancialRecord.id == record_id,
        models.FinancialRecord.is_deleted == False
    ).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    # Soft delete - just mark as deleted, don't actually remove
    record.is_deleted = True
    db.commit()
    return {"message": "Record deleted successfully"}

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from dependencies import require_viewer, require_analyst
import models

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

# Get overall summary (All roles)
@router.get("/summary")
def get_summary(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_viewer)
):
    records = db.query(models.FinancialRecord).filter(
        models.FinancialRecord.is_deleted == False
    ).all()

    total_income = sum(r.amount for r in records if r.type == "income")
    total_expense = sum(r.amount for r in records if r.type == "expense")
    net_balance = total_income - total_expense

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "net_balance": net_balance,
        "total_records": len(records)
    }

# Get category wise totals (Analyst and Admin)
@router.get("/category-totals")
def get_category_totals(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_analyst)
):
    records = db.query(models.FinancialRecord).filter(
        models.FinancialRecord.is_deleted == False
    ).all()

    category_totals = {}
    for record in records:
        if record.category not in category_totals:
            category_totals[record.category] = {"income": 0, "expense": 0}
        category_totals[record.category][record.type] += record.amount

    return category_totals

# Get recent 10 transactions (All roles)
@router.get("/recent-activity")
def get_recent_activity(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_viewer)
):
    records = db.query(models.FinancialRecord).filter(
        models.FinancialRecord.is_deleted == False
    ).order_by(models.FinancialRecord.created_at.desc()).limit(10).all()

    return [
        {
            "id": r.id,
            "amount": r.amount,
            "type": r.type,
            "category": r.category,
            "date": r.date,
            "notes": r.notes
        }
        for r in records
    ]

# Get monthly trends (Analyst and Admin)
@router.get("/monthly-trends")
def get_monthly_trends(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_analyst)
):
    records = db.query(models.FinancialRecord).filter(
        models.FinancialRecord.is_deleted == False
    ).all()

    monthly = {}
    for record in records:
        key = record.date.strftime("%Y-%m")
        if key not in monthly:
            monthly[key] = {"income": 0, "expense": 0}
        monthly[key][record.type] += record.amount

    # Sort by month
    sorted_monthly = dict(sorted(monthly.items()))
    return sorted_monthly

# Get income vs expense breakdown (All roles)
@router.get("/breakdown")
def get_breakdown(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_viewer)
):
    records = db.query(models.FinancialRecord).filter(
        models.FinancialRecord.is_deleted == False
    ).all()

    income_records = [r for r in records if r.type == "income"]
    expense_records = [r for r in records if r.type == "expense"]

    return {
        "income": {
            "count": len(income_records),
            "total": sum(r.amount for r in income_records)
        },
        "expense": {
            "count": len(expense_records),
            "total": sum(r.amount for r in expense_records)
        }
    }
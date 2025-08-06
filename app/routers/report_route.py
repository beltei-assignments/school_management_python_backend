from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import report_schema
from app.services import report_service
from typing import Optional

router = APIRouter(
    tags=["Reports management"],
    prefix="/reports"
)

@router.get("/", response_model=dict)
def get_all_reports(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    student_id: Optional[int] = None,
    subject_id: Optional[int] = None,
    term: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return report_service.get_all_reports(
        db=db,
        page=page,
        limit=limit,
        student_id=student_id,
        subject_id=subject_id,
        term=term
    )

@router.post("/", response_model=dict)
def create_report(
    report: report_schema.ReportCreate,
    db: Session = Depends(get_db)
):
    try:
        report_service.create_report(db=db, report_payload=report)
        return {"success": True, "data": report}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
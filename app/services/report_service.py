from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.progress_report_model import ProgressReport 
from app.schemas import report_schema
from app.utils import paginate

def get_all_reports(
        db: Session,
        page: int = 1,
        limit: int = 10,
        student_id: int = None,
        subject_id: int = None,
        term: str = None,
): 
    skip = paginate.getSkip(page=page, limit=limit)

    query = db.query(ProgressReport).options(
        joinedload(ProgressReport.student),
        joinedload(ProgressReport.subject)
    ).filter(ProgressReport.disabled == False)

    if student_id is not None:
        query = query.filter(ProgressReport.student_id == student_id)
    if subject_id is not None:
        query = query.filter(ProgressReport.subject_id == subject_id)
    if term is not None:
        query = query.filter(ProgressReport.term == term)

    total_count = query.count()
    reports = query.offset(skip).limit(limit).all()

    # Use ReportGet.from_orm() to serialize each report
    report_list = [report_schema.ReportGet.from_orm(report) for report in reports]

    return {
        "count": total_count,
        "rows": report_list
    }

def create_report(
        db: Session,
        report_payload: report_schema.ReportCreate
):
    report_exist = db.query(ProgressReport).filter(ProgressReport.student_id == report_payload.student_id, ProgressReport.subject_id == report_payload.subject_id, ProgressReport.term == report_payload.term).first()
    if report_exist is not None:
        raise HTTPException(status_code=409, detail="Report already exists")
    payload = report_payload.dict()
    new_report = ProgressReport(**payload)
    db.add(new_report)

    try:
        db.commit()
        db.refresh(new_report)
    except IntegrityError as e:
        db.rollback()
        print(f"Database Error: {e}")
    return new_report

def update_report(
        db: Session,
        report_id: int,
        report_payload: report_schema.ReportUpdate
):
    try:
        report = db.query(ProgressReport).filter(ProgressReport.disabled == False, ProgressReport.id == report_id).first()
        if report is None:
            raise HTTPException(status_code=404, detail="Report not found!")
        for key, value in report_payload.dict(exclude_unset=True).items():
            setattr(report, key, value)
        db.commit()
        db.refresh(report)
        return report
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error updating report!")
    except Exception as e:
        db.rollback()
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=400, detail="An unexpected error occured")
    
def delete_report(
        db: Session,
        report_id: int
):
    report = db.query(ProgressReport).filter(ProgressReport.disabled == False, ProgressReport.id == report_id).first()
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found!")
    report.disabled = True
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error deleting report!")
    return report
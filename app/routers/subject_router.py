from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.schemas.subject_schema import SubjectCreate, SubjectUpdate, SubjectsPaginationResponse, SubjectResponse
from app.services import subject_service

router = APIRouter(tags=["Subjects management"])
router.prefix = "/subjects"

@router.get("/", response_model=SubjectsPaginationResponse)
def get_all_subjects(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    name: Optional[str] = None,
    db: Session = Depends(get_db),
):
    subjects, count = subject_service.get_all_subjects(db=db, page=page, limit=limit, name=name)
    return {"count": count, "rows": subjects}

@router.get("/{subject_id}", response_model=SubjectResponse)
def get_subject_by_id(subject_id: int, db: Session = Depends(get_db)):
    subject = subject_service.get_subject_by_id(db=db, subject_id=subject_id)
    if not subject:
        pass
    return subject

@router.post("/")
def create_subject(subject: SubjectCreate, db: Session = Depends(get_db)):
    subject_service.create_subject(db=db, subjectPayload=subject)
    return {"success": True}

@router.put("/{subject_id}")
def update_subject(subject_id: int, subject: SubjectUpdate, db: Session = Depends(get_db)):
    subject_service.update_subject(db=db, subject_id=subject_id, subjectPayload=subject)
    return {"success": True}

@router.delete("/{subject_id}")
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    subject_service.delete_subject(db=db, subject_id=subject_id)
    return {"success": True}

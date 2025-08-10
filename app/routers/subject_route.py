from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import subject_schema
from app.services import subject_service

router = APIRouter(tags=["Subjects management"])
router.prefix = "/subjects"


@router.get("/")
def get_all_subjects(
    page: int = 1,
    limit: int = 10,
    id: str = None,
    name: str = None,
    db: Session = Depends(get_db),
):
    subjects, count = subject_service.get_all_subjects(
        db=db, page=page, limit=limit, id=id, name=name
    )

    return {"count": count, "rows": subjects}


@router.get("/{subject_id}")
def get_subject_id(subject_id: int, db: Session = Depends(get_db)):
    data = subject_service.get_subject_id(db=db, subject_id=subject_id)
    return {"success": True, "data": data}


@router.post("/")
def create_subject(
    subject: subject_schema.SubjectCreate, db: Session = Depends(get_db)
):
    subject_service.create_subject(db=db, subject_payload=subject)
    return {"Success": True, "data": subject}


@router.put("/{subject_id}")
def update_subject(
    subject_id: int,
    subject: subject_schema.SubjectUpdate,
    db: Session = Depends(get_db),
):
    subject_service.update_subject(
        db=db, subject_id=subject_id, subject_payload=subject
    )
    return {"success": True, "data": subject}


@router.delete("/{subject_id}")
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    subject_service.delete_subject(db=db, subject_id=subject_id)
    return {"success": True, "message": "Subject deleted successfully"}

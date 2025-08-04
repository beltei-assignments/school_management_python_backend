from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.subject_model import Subject
from app.schemas import subject_schema
from app.utils import paginate

def get_all_subjects(
        db: Session,
        page: int = 1,
        limit: int = 10,
        name: str = None
):
    skip  = paginate.getSkip(page=page, limit=limit)
    query = db.query(Subject).filter(Subject.disabled == False)

    if name:
        query = query.filter(Subject.name.ilike(f"%{name}%"))

    count = query.count()
    subjects = query.offset(skip).limit(limit).all()

    subjects_mapped = [subject_schema.SubjectGet.from_orm(subject) for subject in subjects]
    return subjects_mapped, count

def get_subject_id(
        db: Session,
        subject_id: int
):
    subject = db.query(Subject).filter(Subject.disabled == False, Subject.id == subject_id).first()
    if subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")
    return {"subject": subject_schema.SubjectGet.from_orm(subject)}

def create_subject(
        db: Session,
        subject_payload: subject_schema.SubjectCreate
):
    subject_exist = db.query(Subject).filter(Subject.name == subject_payload.name).first()
    if subject_exist is not None:
        raise HTTPException(status_code=409, detail="Subject already exists")
    payload = subject_payload.dict()
    new_subject = Subject(**payload)
    db.add(new_subject)
    try:
        db.commit()
        db.refresh(new_subject)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error creating subject")
    return new_subject

def update_subject(
        db: Session,
        subject_id: int,
        subject_payload: subject_schema.SubjectUpdate
):
    try:
        subject = db.query(Subject).filter(Subject.disabled == False, Subject.id == subject_id).first()
        if subject is None:
            raise HTTPException(status_code=404, detail="Subject not found")
        for key, value in subject_payload.dict(exclude_unset=True).items():
            setattr(subject, key, value)

        db.commit()
        db.refresh(subject)
        return subject
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error updating subject")
    except Exception as e:
        db.rollback()
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occured")

def delete_subject(
        db: Session,
        subject_id: int
):
    subject = db.query(Subject).filter(Subject.disabled == False, Subject.id == subject_id).first()
    if subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")
    subject.disabled = True
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error deleting subject")
    
    return {"success": True, "message": "Subject deleted successfully"}
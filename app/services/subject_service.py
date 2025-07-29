from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.subject_model import Subject
from app.schemas.subject_schema import SubjectCreate, SubjectUpdate

def get_all_subjects(db: Session, page: int, limit: int, name: str = None):
    query = db.query(Subject)
    if name:
        query = query.filter(Subject.name.ilike(f"%{name}%"))
    total = query.count()
    subjects = query.offset((page - 1) * limit).limit(limit).all()

    return subjects, total

def get_subject_by_id(db: Session, subject_id: int):
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(
            status_code=404,
            detail=[{"loc": ["path", "subject_id"], "msg": "Subject not found", "type": "value_error.not_found"}]
        )
    return subject

def create_subject(db: Session, subjectPayload: SubjectCreate):
    name = subjectPayload.name.strip()
    if not name:
        raise HTTPException(
            status_code=400,
            detail=[{"loc": ["body", "name"], "msg": "Subject name must not be empty", "type": "value_error"}]
        )
    existing = db.query(Subject).filter(Subject.name == name).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail=[{"loc": ["body", "name"], "msg": "Subject name must be unique", "type": "value_error"}]
        )
    subject = Subject(name=name)
    db.add(subject)
    db.commit()
    db.refresh(subject)
    return subject

def update_subject(db: Session, subject_id: int, subjectPayload: SubjectUpdate):
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(
            status_code=404,
            detail=[{"loc": ["path", "subject_id"], "msg": "Subject not found", "type": "value_error.not_found"}]
        )
    
    name = subjectPayload.name.strip()
    if not name:
        raise HTTPException(
            status_code=400,
            detail=[{"loc": ["body", "name"], "msg": "Subject name must not be empty", "type": "value_error"}]
        )

    existing = db.query(Subject).filter(Subject.name == name, Subject.id != subject_id).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail=[{"loc": ["body", "name"], "msg": "Subject name must be unique", "type": "value_error"}]
        )

    subject.name = name
    db.commit()
    db.refresh(subject)
    return subject

def delete_subject(db: Session, subject_id: int):
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(
            status_code=404,
            detail=[{"loc": ["path", "subject_id"], "msg": "Subject not found", "type": "value_error.not_found"}]
        )
    db.delete(subject)
    db.commit()
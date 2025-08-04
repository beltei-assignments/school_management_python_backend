from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.class_model import Class
from app.schemas.class_schema import ClassCreate, ClassUpdate
from app.utils import paginate


def get_all_classes(db: Session, page: int, limit: int, name: str = None):
    skip = paginate.getSkip(page=page, limit=limit)
    query = db.query(Class).filter(Class.disabled == False)

    if name:
        query = query.filter(Class.name.ilike(f"%{name}%"))
    total = query.count()
    classes = query.offset(skip).limit(limit).all()

    return classes, total


def get_class_by_id(db: Session, class_id: int):
    cls = db.query(Class).filter(Class.id == class_id).first()
    if not cls:
        raise HTTPException(status_code=404, detail="Class not found")
    return cls


def create_class(db: Session, classPayload: ClassCreate):
    name = classPayload.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="Class name must not be empty")

    existing = db.query(Class).filter(Class.name == name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Class name must be unique")

    cls = Class(name=name)
    db.add(cls)
    db.commit()
    db.refresh(cls)
    return cls


def update_class(db: Session, class_id: int, classPayload: ClassUpdate):
    cls = db.query(Class).filter(Class.id == class_id).first()
    if not cls:
        raise HTTPException(status_code=404, detail="Class not found")

    name = classPayload.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="Class name must not be empty")

    existing = db.query(Class).filter(Class.name == name, Class.id != class_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Class name must be unique")

    cls.name = name
    db.commit()
    db.refresh(cls)
    return cls


def delete_class(db: Session, class_id: int):
    cls = db.query(Class).filter(Class.id == class_id, Class.disabled == False).first()
    if not cls:
        raise HTTPException(status_code=404, detail="Class not found")

    cls.disabled = True
    db.commit()

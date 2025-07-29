from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.class_model import Class
from app.schemas.class_schema import ClassCreate, ClassUpdate


def get_all_classes(db: Session, page: int, limit: int, name: str = None):
    query = db.query(Class)
    if name:
        query = query.filter(Class.name.ilike(f"%{name}%"))
    total = query.count()
    classes = query.offset((page - 1) * limit).limit(limit).all()
    return classes, total


def get_class_by_id(db: Session, class_id: int):
    cls = db.query(Class).filter(Class.id == class_id).first()
    if not cls:
        raise HTTPException(
            status_code=404,
            detail=[{
                "loc": ["path", "class_id"],
                "msg": "Class not found",
                "type": "value_error.not_found"
            }]
        )
    return cls


def create_class(db: Session, classPayload: ClassCreate):
    name = classPayload.name.strip()
    if not name:
        raise HTTPException(
            status_code=400,
            detail=[{
                "loc": ["body", "name"],
                "msg": "Class name must not be empty",
                "type": "value_error"
            }]
        )

    existing = db.query(Class).filter(Class.name == name).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail=[{
                "loc": ["body", "name"],
                "msg": "Class name must be unique",
                "type": "value_error"
            }]
        )

    cls = Class(name=name)
    db.add(cls)
    db.commit()
    db.refresh(cls)
    return cls


def update_class(db: Session, class_id: int, classPayload: ClassUpdate):
    cls = db.query(Class).filter(Class.id == class_id).first()
    if not cls:
        raise HTTPException(
            status_code=404,
            detail=[{
                "loc": ["path", "class_id"],
                "msg": "Class not found",
                "type": "value_error.not_found"
            }]
        )

    name = classPayload.name.strip()
    if not name:
        raise HTTPException(
            status_code=400,
            detail=[{
                "loc": ["body", "name"],
                "msg": "Class name must not be empty",
                "type": "value_error"
            }]
        )

    existing = db.query(Class).filter(Class.name == name, Class.id != class_id).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail=[{
                "loc": ["body", "name"],
                "msg": "Class name must be unique",
                "type": "value_error"
            }]
        )

    cls.name = name
    db.commit()
    db.refresh(cls)
    return cls


def delete_class(db: Session, class_id: int):
    cls = db.query(Class).filter(Class.id == class_id).first()
    if not cls:
        raise HTTPException(
            status_code=404,
            detail=[{
                "loc": ["path", "class_id"],
                "msg": "Class not found",
                "type": "value_error.not_found"
            }]
        )
    cls.disabled = True
    db.commit()

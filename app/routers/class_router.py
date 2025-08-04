from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.schemas.class_schema import (
    ClassCreate,
    ClassUpdate,
    ClassesPaginationResponse,
    ClassResponse,
)
from app.services import class_service

router = APIRouter(tags=["Class Management"])
router.prefix = "/classes"


@router.get("/", response_model=ClassesPaginationResponse)
def get_all_classes(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    name: Optional[str] = None,
    db: Session = Depends(get_db),
):
    classes, count = class_service.get_all_classes(
        db=db, page=page, limit=limit, name=name
    )
    return {"count": count, "rows": classes}


@router.get("/{class_id}", response_model=ClassResponse)
def get_class_by_id(class_id: int, db: Session = Depends(get_db)):
    class_ = class_service.get_class_by_id(db=db, class_id=class_id)
    if not class_:
        raise HTTPException(status_code=404, detail="Class not found")
    return class_


@router.post("/")
def create_class(class_data: ClassCreate, db: Session = Depends(get_db)):
    class_service.create_class(db=db, classPayload=class_data)
    return {"success": True}


@router.put("/{class_id}")
def update_class(class_id: int, class_data: ClassUpdate, db: Session = Depends(get_db)):
    class_service.update_class(db=db, class_id=class_id, classPayload=class_data)
    return {"success": True}


@router.delete("/{class_id}")
def delete_class(class_id: int, db: Session = Depends(get_db)):
    class_service.delete_class(db=db, class_id=class_id)
    return {"success": True}

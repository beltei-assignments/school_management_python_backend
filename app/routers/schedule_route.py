from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.services.schedule_service import (
    get_schedules,
    create_schedule,
    update_schedule,
    delete_schedule,
)
from app.schemas.schedule_schema import ScheduleCreate, ScheduleResponseItem

router = APIRouter(prefix="/schedules", tags=["Schedules"])


@router.get("/", response_model=dict)
def read_schedules(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100),
    id: str = None,
    class_id: int = None,
    subject_id: int = None,
    teacher_id: int = None,
):
    data = get_schedules(db, page, limit, id, class_id, subject_id, teacher_id)
    return {
        "count": data["count"],
        "rows": [ScheduleResponseItem.from_orm(cs) for cs in data["rows"]],
    }


@router.post("/")
def create_new_schedule(data: ScheduleCreate, db: Session = Depends(get_db)):
    return create_schedule(db, data)


@router.put("/{schedule_id}")
def update_existing_schedule(
    schedule_id: int = Path(..., ge=1),
    data: ScheduleCreate = None,
    db: Session = Depends(get_db),
):
    return update_schedule(db, schedule_id, data)


@router.delete("/{schedule_id}")
def delete_existing_schedule(
    schedule_id: int = Path(..., ge=1), db: Session = Depends(get_db)
):
    return delete_schedule(db, schedule_id)

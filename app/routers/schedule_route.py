from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.schedule_service import get_schedules, create_schedule
from app.schemas.schedule_schema import ScheduleCreate, ScheduleResponseItem
from typing import List

router = APIRouter(prefix="/schedules", tags=["Schedules"])

@router.get("/", response_model=dict)
def read_schedules(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100),
    class_id: int = None,
    subject_id: int = None,
    teacher_id: int = None,
):
    data = get_schedules(db, page, limit, class_id, subject_id, teacher_id)
    return {
        "count": data["count"],
        "rows": [ScheduleResponseItem.from_orm(cs) for cs in data["rows"]]
    }

@router.post("/")
def create_new_schedule(data: ScheduleCreate, db: Session = Depends(get_db)):
    return create_schedule(db, data)

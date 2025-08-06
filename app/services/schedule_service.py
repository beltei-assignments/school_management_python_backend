from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError

from app.models.schedule_model import Schedule, ClassSubject
from app.schemas.schedule_schema import ScheduleCreate


def get_schedules(db: Session, page: int, limit: int, class_id=None, subject_id=None, teacher_id=None):
    query = db.query(ClassSubject).options(
        joinedload(ClassSubject.class_),
        joinedload(ClassSubject.subject),
        joinedload(ClassSubject.teacher),
        joinedload(ClassSubject.schedules)
    )

    if class_id:
        query = query.filter(ClassSubject.class_id == class_id)
    if subject_id:
        query = query.filter(ClassSubject.subject_id == subject_id)
    if teacher_id:
        query = query.filter(ClassSubject.teacher_id == teacher_id)

    total = query.count()
    rows = query.offset((page - 1) * limit).limit(limit).all()

    return {"count": total, "rows": rows}


def create_schedule(db: Session, data: ScheduleCreate):
    # Manual validation for required fields
    if not data.class_id:
        raise HTTPException(status_code=400, detail="Class id must not be empty")
    if not data.subject_id:
        raise HTTPException(status_code=400, detail="Subject id must not be empty")
    if not data.teacher_id:
        raise HTTPException(status_code=400, detail="Teacher id must not be empty")
    if not data.schedules or len(data.schedules) == 0:
        raise HTTPException(status_code=400, detail="At least one schedule must not be empty")

    for sched in enumerate(data.schedules):
        if not sched.day_of_week or sched.day_of_week.strip() == "":
            raise HTTPException(status_code=422, detail="Day of week must not be empty")

        if sched.start_time == sched.end_time:
            raise HTTPException(status_code=422, detail="Start time and end time cannot be the same")

        if sched.end_time < sched.start_time:
            raise HTTPException(status_code=422, detail="End time must be after start time")

    # Find or create ClassSubject
    class_subject = db.query(ClassSubject).filter_by(
        class_id=data.class_id,
        subject_id=data.subject_id,
        teacher_id=data.teacher_id
    ).first()

    if not class_subject:
        class_subject = ClassSubject(
            class_id=data.class_id,
            subject_id=data.subject_id,
            teacher_id=data.teacher_id
        )
        db.add(class_subject)
        db.commit()
        db.refresh(class_subject)

    created_schedules = []

    for sched in data.schedules:
        # Prevent duplicate schedules
        existing = db.query(Schedule).filter_by(
            class_subject_id=class_subject.id,
            day_of_week=sched.day_of_week,
            start_time=sched.start_time,
            end_time=sched.end_time
        ).first()

        if existing:
            raise HTTPException(
                status_code=409,
                detail=f"Schedule already exists: {sched.day_of_week} from {sched.start_time} to {sched.end_time}"
            )

        schedule_entry = Schedule(
            class_subject_id=class_subject.id,
            day_of_week=sched.day_of_week.strip(),
            start_time=sched.start_time,
            end_time=sched.end_time
        )
        db.add(schedule_entry)
        created_schedules.append(schedule_entry)

    try:
        db.commit()
        for sched in created_schedules:
            db.refresh(sched)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error creating schedule")

    return {"success": True, "created": len(created_schedules)}
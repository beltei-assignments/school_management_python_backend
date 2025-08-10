from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError

from app.models.schedule_model import Schedule, ClassSubject
from app.schemas.schedule_schema import ScheduleCreate


def get_schedules(db: Session, page: int = 1, limit: int = 10, class_id=None, subject_id=None, teacher_id=None):
    if page < 1:
        page = 1
    if limit < 1:
        limit = 10

    query = (
        db.query(ClassSubject)
        .join(ClassSubject.schedules)
        .filter(
            ClassSubject.disabled == False,
            Schedule.disabled == False,
        )
        .options(
            joinedload(ClassSubject.class_),
            joinedload(ClassSubject.subject),
            joinedload(ClassSubject.teacher),
            joinedload(ClassSubject.schedules.and_(Schedule.disabled == False))
        )
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
    if not data.class_id:
        raise HTTPException(status_code=400, detail="Class id must not be empty")
    if not data.subject_id:
        raise HTTPException(status_code=400, detail="Subject id must not be empty")
    if not data.teacher_id:
        raise HTTPException(status_code=400, detail="Teacher id must not be empty")
    if not data.schedules or len(data.schedules) == 0:
        raise HTTPException(status_code=400, detail="At least one schedule must be provided")

    for sched in data.schedules:
        if sched.start_time == sched.end_time:
            raise HTTPException(status_code=422, detail="Start time and end time cannot be the same")
        if sched.end_time < sched.start_time:
            raise HTTPException(status_code=422, detail="End time must be after start time")

    class_subject = db.query(ClassSubject).filter_by(
        class_id=data.class_id,
        subject_id=data.subject_id,
        teacher_id=data.teacher_id,
        disabled=False
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
        day_of_week = sched.day_of_week.strip()
        conflict = db.query(Schedule).filter(
            Schedule.class_subject_id == class_subject.id,
            Schedule.day_of_week == day_of_week,
            Schedule.start_time < sched.end_time,
            Schedule.end_time > sched.start_time,
            Schedule.disabled == False
        ).first()

        if conflict:
            raise HTTPException(
                status_code=409,
                detail=f"Schedule conflict: overlaps with existing schedule on {day_of_week} "
                       f"from {conflict.start_time} to {conflict.end_time}"
            )

        schedule_entry = Schedule(
            class_subject_id=class_subject.id,
            day_of_week=day_of_week,
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

    return {"success": True}


def update_schedule(db: Session, schedule_id: int, data: ScheduleCreate):
    schedule = db.query(Schedule).filter(
        Schedule.id == schedule_id,
        Schedule.disabled == False
    ).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")

    if not data.class_id:
        raise HTTPException(status_code=400, detail="Class id must not be empty")
    if not data.subject_id:
        raise HTTPException(status_code=400, detail="Subject id must not be empty")
    if not data.teacher_id:
        raise HTTPException(status_code=400, detail="Teacher id must not be empty")
    if not data.schedules or len(data.schedules) != 1:
        raise HTTPException(status_code=400, detail="Exactly one schedule must be provided for update")

    sched = data.schedules[0]
    if sched.start_time == sched.end_time:
        raise HTTPException(status_code=422, detail="Start time and end time cannot be the same")
    if sched.end_time < sched.start_time:
        raise HTTPException(status_code=422, detail="End time must be after start time")

    class_subject = db.query(ClassSubject).filter_by(
        class_id=data.class_id,
        subject_id=data.subject_id,
        teacher_id=data.teacher_id,
        disabled=False
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

    conflict = db.query(Schedule).filter(
        Schedule.class_subject_id == class_subject.id,
        Schedule.day_of_week == sched.day_of_week.strip(),
        Schedule.start_time < sched.end_time,
        Schedule.end_time > sched.start_time,
        Schedule.id != schedule.id,
        Schedule.disabled == False
    ).first()

    if conflict:
        raise HTTPException(
            status_code=409,
            detail=f"Schedule conflict: overlaps with existing schedule on {sched.day_of_week} "
                   f"from {conflict.start_time} to {conflict.end_time}"
        )

    schedule.class_subject_id = class_subject.id
    schedule.day_of_week = sched.day_of_week.strip()
    schedule.start_time = sched.start_time
    schedule.end_time = sched.end_time

    try:
        db.commit()
        db.refresh(schedule)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error updating schedule")

    return {"success": True}


def delete_schedule(db: Session, schedule_id: int):
    schedule = db.query(Schedule).filter(
        Schedule.id == schedule_id,
        Schedule.disabled == False
    ).first()

    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")

    schedule.disabled = True
    db.commit()

    return {"success": True}

from sqlalchemy.orm import Session
from datetime import datetime
from app.models.schedule_model import Schedule, ClassSubject

def seed_schedules(db: Session):
    try:
        if db.query(Schedule).first():
            return

        class_subject = db.query(ClassSubject).first()
        if not class_subject:
            return

        schedules = [
            {
                "class_subject_id": class_subject.id,
                "day_of_week": "Monday",
                "start_time": datetime(2025, 8, 7, 8, 0),
                "end_time": datetime(2025, 8, 7, 9, 0),
            },
            {
                "class_subject_id": class_subject.id,
                "day_of_week": "Wednesday",
                "start_time": datetime(2025, 8, 7, 10, 0),
                "end_time": datetime(2025, 8, 7, 11, 0),
            },
        ]

        for sched in schedules:
            db.add(Schedule(**sched))
        db.commit()
    finally:
        db.close()

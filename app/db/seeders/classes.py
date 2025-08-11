from sqlalchemy.orm import Session
from app.schemas import class_schema
from app.services import class_service
from app.models.schedule_model import ClassSubject, Schedule


def seed_classes(db: Session):
    print("---> Seeding classes, please wait... <---")

    classes = [
        {
            "name": "A-101",
            "disabled": False,
            "class_subjects": [
                {
                    "subject_id": 1,
                    "teacher_id": 2,
                }
            ],
            "schedules": [
                {
                    "day_of_week": "Monday",
                    "start_time": "2025-08-11 17:30:00",
                    "end_time": "2025-08-11 20:30:00",
                }
            ],
        },
        {
            "name": "B-021",
            "disabled": False,
            "class_subjects": [
                {
                    "subject_id": 2,
                    "teacher_id": 2,
                }
            ],
            "schedules": [
                {
                    "day_of_week": "Tuesday",
                    "start_time": "2025-08-11 17:30:00",
                    "end_time": "2025-08-11 20:30:00",
                }
            ],
        },
        {
            "name": "C-305",
            "disabled": False,
            "class_subjects": [
                {
                    "subject_id": 3,
                    "teacher_id": 2,
                }
            ],
            "schedules": [
                {
                    "day_of_week": "Wednesday",
                    "start_time": "2025-08-11 17:30:00",
                    "end_time": "2025-08-11 20:30:00",
                }
            ],
        },
        {
            "name": "D-110",
            "disabled": False,
            "class_subjects": [
                {
                    "subject_id": 4,
                    "teacher_id": 3,
                }
            ],
            "schedules": [
                {
                    "day_of_week": "Thursday",
                    "start_time": "2025-08-11 17:30:00",
                    "end_time": "2025-08-11 20:30:00",
                }
            ],
        },
        {
            "name": "E-204",
            "disabled": False,
            "class_subjects": [
                {
                    "subject_id": 5,
                    "teacher_id": 3,
                }
            ],
            "schedules": [
                {
                    "day_of_week": "Friday",
                    "start_time": "2025-08-11 17:30:00",
                    "end_time": "2025-08-11 20:30:00",
                }
            ],
        },
        {
            "name": "F-407",
            "disabled": False,
            "class_subjects": [
                {
                    "subject_id": 1,
                    "teacher_id": 3,
                }
            ],
            "schedules": [
                {
                    "day_of_week": "Saturday",
                    "start_time": "2025-08-11 17:30:00",
                    "end_time": "2025-08-11 20:30:00",
                }
            ],
        },
        {
            "name": "G-508",
            "disabled": False,
            "class_subjects": [
                {
                    "subject_id": 1,
                    "teacher_id": 2,
                }
            ],
            "schedules": [
                {
                    "day_of_week": "Sunday",
                    "start_time": "2025-08-11 17:30:00",
                    "end_time": "2025-08-11 20:30:00",
                }
            ],
        },
        {
            "name": "H-102",
            "disabled": True,
            "class_subjects": [
                {
                    "subject_id": 1,
                    "teacher_id": 2,
                }
            ],
            "schedules": [
                {
                    "day_of_week": "Monday",
                    "start_time": "2025-08-11 17:30:00",
                    "end_time": "2025-08-11 20:30:00",
                }
            ],
        },
        {"name": "I-303", "disabled": False, "class_subjects": []},
        {"name": "J-209", "disabled": False, "class_subjects": []},
    ]

    for cls in classes:
        newClass = class_service.create_class(
            db=db,
            classPayload=class_schema.ClassCreate(
                name=cls["name"],
                disabled=cls["disabled"],
            ),
        )

        for cs_data in cls["class_subjects"]:
            cs_data["class_id"] = newClass.id

            newCS = ClassSubject(**cs_data)
            db.add(newCS)
            db.flush()  # ensures newCS.id is generated without committing

            for s_data in cls["schedules"]:
                s_data["class_subject_id"] = newCS.id
                db.add(Schedule(**s_data))
    db.commit()

    print("---> Seeding classes completed. <---")

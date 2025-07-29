from app.database import SessionLocal
from app.schemas import subject_schema
from app.services import subject_service

def seed_subjects():
    subjects = [
        {"name": "Python", "disabled": False},
        {"name": "Java", "disabled": False},
        {"name": "C++", "disabled": False},
        {"name": "JavaScript", "disabled": False},
        {"name": "Dart", "disabled": False},
        {"name": "Go", "disabled": False},
        {"name": "Kotlin", "disabled": False},
        {"name": "SQL", "disabled": True},
        {"name": "HTML", "disabled": False},
        {"name": "CSS", "disabled": False},
    ]

    for subj in subjects:
        subject_service.create_subject(
            db=SessionLocal(),
            subjectPayload=subject_schema.SubjectCreate(
                name=subj["name"],
                disabled=subj["disabled"],
            ),
        )

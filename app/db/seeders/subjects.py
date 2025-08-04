from sqlalchemy.orm import Session
from app.schemas import subject_schema
from app.services import subject_service


def seed_subjects(db: Session):
    print("---> Seeding subjects, please wait... <---")

    subjects = [
        {"name": "Python"},
        {"name": "AI"},
        {"name": "Research Methodology"},
        {"name": "Cloud Computing"},
        {"name": "Mobile Application Development"},
    ]

    for subject in subjects:
        subject_service.create_subject(
            db=db,
            subject_payload=subject_schema.SubjectCreate(
                name=subject["name"],
            ),
        )

    print("---> Seeding subjects completed. <---")

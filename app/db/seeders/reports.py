from sqlalchemy.orm import Session
from app.models.progress_report_model import ProgressReport


def seed_reprts(db: Session):
    reports = [
        {"student_id": 5, "subject_id": 1, "term": "Term 1", "score": 88},
        {"student_id": 6, "subject_id": 1, "term": "Term 1", "score": 90},
        {"student_id": 5, "subject_id": 2, "term": "Term 1", "score": 100},
        {"student_id": 6, "subject_id": 2, "term": "Term 1", "score": 58},
        {"student_id": 5, "subject_id": 3, "term": "Term 1", "score": 88},
        {"student_id": 6, "subject_id": 3, "term": "Term 1", "score": 90},
        {"student_id": 5, "subject_id": 4, "term": "Term 1", "score": 72},
        {"student_id": 6, "subject_id": 4, "term": "Term 1", "score": 81},
        {"student_id": 5, "subject_id": 5, "term": "Term 1", "score": 78},
        {"student_id": 6, "subject_id": 5, "term": "Term 1", "score": 67},
    ]

    print("---> Seeding reports, please wait... <---")

    try:
        for report in reports:
            db.add(ProgressReport(**report))
        db.commit()
    finally:
        db.close()

    print("---> Seeding reports completed. <---")

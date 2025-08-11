from app.database import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.user_model import User
from app.models.role_model import Role
from app.models.user_has_role_model import UserHasRole
from app.models.class_model import Class
from app.models.subject_model import Subject
from app.models.schedule_model import Schedule, ClassSubject
from app.models.progress_report_model import ProgressReport
from app.db.seeders import roles, users, subjects, classes, reports


def seed():
    db = SessionLocal()
    try:
        # Clean all tables before seeding
        clean_all_tables(db=db)

        print("---> Seeding roles and users, please wait... <---")
        roles.seed_roles(db=db)
        users.seed_users(db=db)
        print("---> Seeding roles and users completed. <---")

        subjects.seed_subjects(db=db)
        classes.seed_classes(db=db)
        reports.seed_reprts(db=db)

        db.commit()
    finally:
        db.close()


def clean_all_tables(db: Session):
    print("---> Cleaning all tables, please wait... <---")

    # For many-to-many association tables, use execute
    db.execute(UserHasRole.delete())
    db.query(ProgressReport).delete()
    db.query(Schedule).delete()
    db.query(ClassSubject).delete()
    db.query(User).delete()
    db.query(Role).delete()
    db.query(Class).delete()
    db.query(Subject).delete()

    db.commit()

    # Reset auto-increment counters
    db.execute(text("ALTER TABLE users AUTO_INCREMENT = 1;"))
    db.execute(text("ALTER TABLE roles AUTO_INCREMENT = 1;"))
    db.execute(text("ALTER TABLE classes AUTO_INCREMENT = 1;"))
    db.execute(text("ALTER TABLE subjects AUTO_INCREMENT = 1;"))
    db.execute(text("ALTER TABLE schedules AUTO_INCREMENT = 1;"))
    db.execute(text("ALTER TABLE class_subjects AUTO_INCREMENT = 1;"))
    db.execute(text("ALTER TABLE reports AUTO_INCREMENT = 1;"))
    db.commit()

    print("---> Cleaning all tables completed. <---")


if __name__ == "__main__":
    seed()

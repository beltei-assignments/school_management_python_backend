from app.database import SessionLocal
from app.models.role_model import Role


def seed_roles():
    db = SessionLocal()
    role = [
        {"name": "Admin", "value": "admin"},
        {"name": "Teacher", "value": "teacher"},
        {"name": "Student", "value": "student"},
    ]
    try:
        for r in role:
            db.add(Role(**r))
        db.commit()
    finally:
        db.close()

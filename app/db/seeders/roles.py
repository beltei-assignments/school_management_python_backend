from app.database import SessionLocal
from app.models.role_model import Role


def seed_roles():
    db = SessionLocal()
    roles = [
        {"name": "Admin", "value": "admin"},
        {"name": "Teacher", "value": "teacher"},
        {"name": "Parent", "value": "parent"},
        {"name": "Student", "value": "student"},
    ]
    try:
        for role in roles:
            db.add(Role(**role))
        db.commit()
    finally:
        db.close()

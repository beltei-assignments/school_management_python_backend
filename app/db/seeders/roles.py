from sqlalchemy.orm import Session
from app.models.role_model import Role


def seed_roles(db: Session):
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

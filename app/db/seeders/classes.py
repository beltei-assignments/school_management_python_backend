from app.database import SessionLocal
from app.schemas import class_schema
from app.services import class_service

def seed_classes():
    print("---> Seeding classes, please wait... <---")

    classes = [
        {"name": "A-101", "disabled": False},
        {"name": "B-021", "disabled": False},
        {"name": "C-305", "disabled": False},
        {"name": "D-110", "disabled": False},
        {"name": "E-204", "disabled": False},
        {"name": "F-407", "disabled": False},
        {"name": "G-508", "disabled": False},
        {"name": "H-102", "disabled": True},
        {"name": "I-303", "disabled": False},
        {"name": "J-209", "disabled": False},
    ]

    for cls in classes:
        class_service.create_class(
            db=SessionLocal(),
            classPayload=class_schema.ClassCreate(
                name=cls["name"],
                disabled=cls["disabled"],
            ),
        )

    print("---> Seeding classes completed. <---")

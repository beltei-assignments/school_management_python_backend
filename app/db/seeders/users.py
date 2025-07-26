from app.database import SessionLocal
from app.schemas import user_schema as user_schema
from app.services import user_service as user_service


def seed_users():
    users = [
        {
            "email": "admin@example.com",
            "password": "123",
            "first_name": "Admin",
            "last_name": "User",
            "phone_number": "1234567890",
            "roles_ids": [1],
        },
        {
            "email": "makara@example.com",
            "password": "123",
            "first_name": "Makara",
            "last_name": "Phoem",
            "phone_number": "1234567890",
            "roles_ids": [2],
        },
        {
            "email": "nit@example.com",
            "password": "123",
            "first_name": "Nit",
            "last_name": "Noem",
            "phone_number": "1234567890",
            "roles_ids": [2],
        },
        {
            "email": "dara@example.com",
            "password": "123",
            "first_name": "Dara",
            "last_name": "Sok",
            "phone_number": "1234567890",
            "roles_ids": [3],
        },
        {
            "email": "sok@example.com",
            "password": "123",
            "first_name": "Sok",
            "last_name": "Tep",
            "phone_number": "1234567890",
            "roles_ids": [3],
        },
    ]

    for user in users:
        user_service.create_user(
            db=SessionLocal(),
            userPayload=user_schema.UserCreate(
                email=user["email"],
                password=user["password"],
                first_name=user["first_name"],
                last_name=user["last_name"],
                phone_number=user["phone_number"],
                roles_ids=user["roles_ids"],
            ),
        )

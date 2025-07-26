from app.database import SessionLocal
from sqlalchemy import text
from app.models.user_model import User
from app.models.role_model import Role
from app.models.user_has_role_model import user_has_role
from app.db.seeders.roles import seed_roles
from app.db.seeders.users import seed_users


def seed():
    # Clean all tables before seeding
    clean_all_tables()

    print("---> Seeding roles and users, please wait... <---")
    seed_roles()
    seed_users()
    print("---> Seeding roles and users completed. <---")


def clean_all_tables():
    print("---> Cleaning all tables, please wait... <---")

    db = SessionLocal()
    try:
        # For many-to-many association tables, use execute
        db.execute(user_has_role.delete())
        db.query(User).delete()
        db.query(Role).delete()
        db.commit()

        # Reset auto-increment counters
        db.execute(text("ALTER TABLE users AUTO_INCREMENT = 1;"))
        db.execute(text("ALTER TABLE roles AUTO_INCREMENT = 1;"))
        db.commit()
    finally:
        db.close()

    print("---> Cleaning all tables completed. <---")


if __name__ == "__main__":
    seed()

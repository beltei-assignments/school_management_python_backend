from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user_model import User
from app.utils import jwt, bcrypt
from app.schemas import user_schema


def login(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=401, detail="Incorrect email address or password"
        )
    if not bcrypt.verify_password(
        plain_password=password, hashed_password=user.password
    ):
        raise HTTPException(
            status_code=401, detail="Incorrect email address or password"
        )

    token = jwt.create_access_token(data={"user_id": user.id})

    return {
        "success": True,
        "token_type": "bearer",
        "token": token,
        "user": user_schema.UserGet.from_orm(user),
        "roles": user.roles,
    }

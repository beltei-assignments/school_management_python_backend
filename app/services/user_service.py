from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.user_model import User
from app.schemas import user_schema
from app.utils import bcrypt


def get_all_users(db: Session, skip: int = 0, limit: int = 10):
    query = db.query(User)
    count = query.count()
    users = query.offset(skip).limit(limit).all()

    users_out = [user_schema.UserBase.from_orm(u) for u in users]

    return users_out, count


def get_user_by_id(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


def create_user(db: Session, userPayload: user_schema.UserBase):
    userExist = db.query(User).filter(User.email == userPayload.email).first()
    if userExist is not None:
        raise HTTPException(status_code=409, detail="Email already exists")

    user_data = userPayload.dict()
    user_data["password"] = bcrypt.hash_password(userPayload.password)
    db_user = User(**user_data)

    db.add(db_user)
    db.commit()
    # db.refresh(db_user)

    return db_user


def update_user(db: Session, user_id: int, userPayload: user_schema.UserUpdate):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if user:
        for key, value in userPayload.dict(exclude_unset=True).items():
            setattr(user, key, value)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="Email already exists")
        db.refresh(user)

    return user


def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if user:
        db.delete(user)
        db.commit()

    return user

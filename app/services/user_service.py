from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.user_model import User
from app.models.role_model import Role
from app.schemas import user_schema
from app.utils import bcrypt, paginate


def get_all_users(
    db: Session,
    page: int = 1,
    limit: int = 10,
    id: str = None,
    email: str = None,
    name: str = None,
    role_id: int = None,
):
    skip = paginate.getSkip(page=page, limit=limit)

    query = db.query(User).filter(User.disabled == False)

    # Filters
    if id is not None and id is not "":
        query = query.filter(User.id == id)
    if email:
        query = query.filter(User.email.ilike(f"%{email}%"))
    if name:
        query = query.filter(
            User.first_name.ilike(f"%{name}%") | User.last_name.ilike(f"%{name}%")
        )
    if role_id:
        query = query.join(User.roles).filter(Role.id == role_id)

    count = query.count()
    users = query.order_by(User.id.desc()).offset(skip).limit(limit).all()

    usersMapped = [
        {'user': user_schema.UserGet.from_orm(u), 'roles': u.roles} for u in users
    ]

    return usersMapped, count


def get_user_by_id(db: Session, user_id: int):
    user = db.query(User).filter(User.disabled == False, User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return {'user': user_schema.UserGet.from_orm(user), 'roles': user.roles}


def create_user(db: Session, userPayload: user_schema.UserCreate):
    userExist = db.query(User).filter(User.email == userPayload.email).first()
    if userExist is not None:
        raise HTTPException(status_code=409, detail="Email already exists")

    rolesToAdd = db.query(Role).filter(Role.id.in_(userPayload.roles_ids)).all()
    if not rolesToAdd or len(rolesToAdd) != len(userPayload.roles_ids):
        raise HTTPException(status_code=400, detail="Invalid role IDs")

    payload = userPayload.dict()
    payload["password"] = bcrypt.hash_password(userPayload.password)
    del payload["roles_ids"]  # Remove roles_ids
    newUser = User(**payload)

    db.add(newUser)
    db.commit()

    newUser.roles = rolesToAdd
    db.commit()  # Commit to save the association
    db.refresh(newUser)

    return newUser


def update_user(db: Session, user_id: int, userPayload: user_schema.UserUpdate):
    user = db.query(User).filter(User.disabled == False, User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in userPayload.dict(exclude_unset=True).items():
        # Hash the password if it is being updated
        if key == "password" and value is not None and value is not "":
            value = bcrypt.hash_password(value)
        if value is not None and value is not "":
            setattr(user, key, value)
    if userPayload.roles_ids is not None:
        rolesToUpdate = db.query(Role).filter(Role.id.in_(userPayload.roles_ids)).all()
        if not rolesToUpdate or len(rolesToUpdate) != len(userPayload.roles_ids):
            raise HTTPException(status_code=400, detail="Invalid role IDs")
        user.roles = rolesToUpdate
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")
    db.refresh(user)

    return user


def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.disabled == False, User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user.disabled = True
    db.commit()

    return user

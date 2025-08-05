from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db, SessionLocal
from app.schemas import user_schema as user_schema
from app.services import user_service as user_service

router = APIRouter(tags=["Users management"])
router.prefix = "/users"


@router.get("/")
def get_all_users(
    page: int = 1,
    limit: int = 10,
    id: str = None,
    email: str = None,
    name: str = None,
    role_id: int = None,
    db: Session = Depends(get_db),
):
    users, count = user_service.get_all_users(
        db=db, page=page, limit=limit, id=id, email=email, name=name, role_id=role_id
    )

    return {"count": count, "rows": users}


@router.get("/{user_id}")
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    data = user_service.get_user_by_id(db=db, user_id=user_id)

    return {"success": True, "data": data}


@router.post("/")
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    user_service.create_user(db=db, userPayload=user)
    return {"success": True}


@router.put("/{user_id}")
def update_user_by_id(
    user_id: int, user: user_schema.UserUpdate, db: Session = Depends(get_db)
):
    user_service.update_user(db=db, user_id=user_id, userPayload=user)
    return {"success": True}


@router.delete("/{user_id}")
def delete_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user_service.delete_user(db=db, user_id=user_id)
    return {"success": True}

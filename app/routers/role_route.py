from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.services import auth_service

router = APIRouter(tags=["Role Management"])
router.prefix = "/roles"


@router.get("/")
def get_all_roles(
    db: Session = Depends(get_db),
):
    return auth_service.get_all_roles(db=db)

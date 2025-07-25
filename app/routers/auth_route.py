from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import user_schema
from app.services import auth_service

router = APIRouter(tags=["Authentications"])

prefix = "/api/auth"
router.prefix = prefix


@router.post("/login/")
def login(body: user_schema.Login, db: Session = Depends(get_db)):
    return auth_service.login(db, body.email, body.password)

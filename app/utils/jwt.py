from jose import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire_days = int(
        os.getenv("JWT_ACCESS_TOKEN_EXPIRE_DAYS", 1)
    )  # default to 1 day if not set
    expire = datetime.utcnow() + (expires_delta or timedelta(days=expire_days))
    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode, os.getenv("JWT_SECRET_KEY"), algorithm=os.getenv("JWT_ALGORITHM")
    )

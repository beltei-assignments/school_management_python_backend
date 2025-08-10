from pydantic import BaseModel
from typing import Optional


class Login(BaseModel):
    email: str
    password: str


class UserBase(BaseModel):
    id: Optional[int] = None
    email: str
    first_name: str
    last_name: str
    password: str
    phone_number: Optional[str] = None
    disabled: Optional[bool] = False

    class Config:
        from_attributes = True


class UserGet(BaseModel):
    id: Optional[int] = None
    email: str
    first_name: str
    last_name: str
    phone_number: str
    disabled: bool

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    password: str
    roles_ids: list[int]


class UserUpdate(UserBase):
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    roles_ids: list[int]

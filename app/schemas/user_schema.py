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


class UserBase(BaseModel):
    id: Optional[int] = None
    email: str
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
    disabled: Optional[bool] = False

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class User(UserBase):
    id: int

    class Config:
        orm_mode = True

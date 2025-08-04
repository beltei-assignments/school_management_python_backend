from pydantic import BaseModel
from typing import Optional


class SubjectBase(BaseModel):
    name: str
    disabled: Optional[bool] = False

    class Config:
        from_attributes = True


class SubjectGet(BaseModel):
    id: Optional[int] = None
    name: str
    disabled: bool

    class Config:
        from_attributes = True


class SubjectCreate(SubjectBase):
    pass


class SubjectUpdate(SubjectBase):
    name: Optional[str] = None
    disabled: Optional[bool] = None

    class Config:
        from_attributes = True

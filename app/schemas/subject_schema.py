from pydantic import BaseModel
from typing import Optional


class SubjectBase(BaseModel):
    name: str
    disabled: Optional[bool] = False

    class Config:
        from_attributes = True  # updated for Pydantic v2


class SubjectCreate(SubjectBase):
    pass


class SubjectUpdate(BaseModel):
    name: Optional[str] = None
    disabled: Optional[bool] = None

    class Config:
        from_attributes = True  # updated for Pydantic v2


class SubjectGet(BaseModel):
    id: Optional[int] = None
    name: str
    disabled: bool

    class Config:
        from_attributes = True  # updated for Pydantic v2

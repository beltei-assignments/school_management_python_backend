from typing import List
from pydantic import BaseModel

class ClassBase(BaseModel):
    name: str

class ClassCreate(ClassBase):
    pass

class ClassUpdate(ClassBase):
    pass

class ClassResponse(BaseModel):
    id: int
    name: str
    disabled: bool = False

    class Config:
        orm_mode = True

class ClassesPaginationResponse(BaseModel):
    count: int
    rows: List[ClassResponse]

    class Config:
        orm_mode = True

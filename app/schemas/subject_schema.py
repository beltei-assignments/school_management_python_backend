from typing import List, Optional
from pydantic import BaseModel

class SubjectBase(BaseModel):
    name: str

class SubjectCreate(SubjectBase):
    pass

class SubjectUpdate(SubjectBase):
    pass

class SubjectResponse(BaseModel):
    id: int
    name: str
    disabled: bool 
    
    class Config:
        orm_mode = True

class SubjectsPaginationResponse(BaseModel):
    count: int
    rows: List[SubjectResponse]

    class Config:
        orm_mode = True

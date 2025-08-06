from pydantic import BaseModel
from typing import Optional
from app.schemas.user_schema import UserGet
from app.schemas.subject_schema import SubjectGet

class ReportBase(BaseModel):
    student_id: int
    subject_id: int
    term: str
    score: float
    disabled: Optional[bool] = False

    class Config:
        from_attributes = True

class ReportGet(BaseModel):
    id: Optional[int] = None
    student_id: int
    subject_id: int
    term: str
    score: float
    disabled: bool
    student: Optional[UserGet]
    subject: Optional[SubjectGet]

    class Config:
        from_attributes = True

class ReportCreate(BaseModel):
    student_id: int
    subject_id: int
    term: str
    score: float
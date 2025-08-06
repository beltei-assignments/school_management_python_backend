from pydantic import BaseModel
from typing import List
from datetime import datetime

class ScheduleEntry(BaseModel):
    day_of_week: str
    start_time: datetime
    end_time: datetime

class ScheduleCreate(BaseModel):
    class_id: int
    subject_id: int
    teacher_id: int
    schedules: List[ScheduleEntry]

class ScheduleRow(BaseModel):
    id: int
    day_of_week: str
    start_time: datetime
    end_time: datetime

    class Config:
        from_attributes = True

class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str

    class Config:
        from_attributes = True

class SubjectOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class ClassOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class ScheduleResponseItem(BaseModel):
    id: int
    class_id: int
    subject_id: int
    teacher_id: int
    disabled: bool = False
    class_: ClassOut
    subject: SubjectOut
    teacher: UserOut
    schedules: List[ScheduleRow]

    class Config:
        from_attributes = True

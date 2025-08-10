from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class ClassSubject(Base):
    __tablename__ = "class_subjects"
    id = Column(Integer, primary_key=True, autoincrement=True)
    class_id = Column(Integer, ForeignKey("classes.id"))
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    teacher_id = Column(Integer, ForeignKey("users.id"))
    disabled = Column(Boolean, default=False)

    class_ = relationship("Class", backref="class_subjects")
    subject = relationship("Subject", backref="class_subjects")
    teacher = relationship("User", backref="class_subjects")
    schedules = relationship("Schedule", back_populates="class_subject", cascade="all, delete")

class Schedule(Base):
    __tablename__ = "schedules"
    id = Column(Integer, primary_key=True, autoincrement=True)
    class_subject_id = Column(Integer, ForeignKey("class_subjects.id"))
    day_of_week = Column(String(20), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    disabled = Column(Boolean, default=False)

    class_subject = relationship("ClassSubject", back_populates="schedules")

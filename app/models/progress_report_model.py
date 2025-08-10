from sqlalchemy import Column, Integer, String, Boolean, Numeric, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship


class ProgressReport(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    term = Column(String(255), nullable=False)
    score = Column(Numeric, nullable=False)
    disabled = Column(Boolean, default=False)

    student = relationship("User", back_populates="reports")
    subject = relationship("Subject", back_populates="reports")

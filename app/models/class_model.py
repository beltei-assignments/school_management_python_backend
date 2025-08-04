from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base


class Class(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    disabled = Column(Boolean, default=False)

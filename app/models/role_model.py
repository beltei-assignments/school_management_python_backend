from sqlalchemy import Column, Integer, String
from app.models.user_has_role_model import UserHasRole
from sqlalchemy.orm import relationship

from app.database import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True)
    value = Column(String(255), unique=True)

    # Define the relationship
    users = relationship("User", secondary=UserHasRole, back_populates="roles")

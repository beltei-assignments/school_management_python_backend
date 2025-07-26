from sqlalchemy import Boolean, Column, Integer, String
from app.models.user_has_role_model import UserHasRole
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True)
    password = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    phone_number = Column(String(255), nullable=True)
    disabled = Column(Boolean, nullable=True, default=False)

    # Define the relationship
    roles = relationship("Role", secondary=UserHasRole, back_populates="users")

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.session import Base


class RoleModel(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)

    users = relationship("UserModel", back_populates="role")
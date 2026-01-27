from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from db.session import Base


class UserModel(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

    role_id = Column(Integer, ForeignKey("role.id"))
    role = relationship("RoleModel", back_populates="users")

    events = relationship("EventModel", back_populates="users", secondary="user_event")
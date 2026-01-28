from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean

from db.base import Base


class UserModel(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    is_active = Column(Boolean, default=True)
    email = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
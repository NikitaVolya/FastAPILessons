from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from db.session import Base



class EventModel(Base):
    __tablename__ = "event"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    datetime = Column(DateTime, nullable=False)

    departament_id = Column(Integer, ForeignKey("departament.id"))
    departament = relationship("DepartamentModel", back_populates="events")

    users = relationship("UserModel", back_populates="events", secondary="user_event")

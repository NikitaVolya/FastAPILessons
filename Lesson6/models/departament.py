from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from db.session import Base


class DepartamentModel(Base):
    __tablename__ = "departament"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)

    events = relationship("EventModel", back_populates="departament")

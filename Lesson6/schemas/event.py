from pydantic import BaseModel, Field
from datetime import datetime

from schemas.departament import DepartamentRead
from schemas.user import UserRead


class EventCreate(BaseModel):

    name: str = Field(min_length=3, max_length=50)
    datetime: datetime
    departament_id: int


class EventRead(EventCreate):
    id: int
    users: list[UserRead] = []

class EventSmall(BaseModel):
    id: int
    name: str = Field(min_length=3, max_length=50)
    datetime: datetime
    departament_id: int
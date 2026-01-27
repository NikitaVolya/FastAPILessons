from typing import List

from sqlalchemy.orm import Session
from datetime import datetime

from models.event import EventModel
from models.user import UserModel

class EventRepository:

    def create(self, db: Session, name: str, event_datetime: datetime, departament_id: int) -> EventModel:

        event = EventModel(name=name, datetime=event_datetime, departament_id=departament_id)

        db.add(event)
        db.commit()
        db.refresh(event)
        return event

    def add_event_user(self, db: Session, event_id: int, user_id: int) -> EventModel:
        event = db.query(EventModel).filter(EventModel.id == event_id).first()
        user = db.query(UserModel).filter(UserModel.id == user_id).first()

        event.users.append(user)
        db.commit()
        db.refresh(event)
        return event

    def get_events_by_user_id(self, db: Session, user_id: int) -> List[EventModel]:
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        return user.events

    def get_event_by_id(self, db: Session, event_id: int) -> EventModel:
        return db.query(EventModel).filter(EventModel.id == event_id).first()

    def get_all(self, db: Session) -> list[EventModel]:
        return db.query(EventModel).all()
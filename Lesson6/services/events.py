from typing import List

from sqlalchemy.orm import Session

from models import EventModel
from repositories.departaments import DepartamentRepository
from repositories.events import EventRepository
from repositories.users import UserRepository
from schemas.event import EventCreate, EventRead
from schemas.user import UserRead
from services.departaments import DepartamentService


class EventService:

    def __init__(self, repository: EventRepository):
        self.__repository: EventRepository = repository

    @staticmethod
    def get_event_read(event: EventModel) -> EventRead:
        return EventRead(
            id=event.id,
            name=event.name,
            datetime=event.datetime,
            departament_id=event.departament_id,
            users=[UserRead(id=user.id,
                            first_name=user.first_name,
                            last_name=user.last_name,
                            role_name=user.role.name) for user in event.users]
        )

    def register(self, db: Session, event: EventCreate) -> EventRead:
        departament_service = DepartamentService(DepartamentRepository())

        if departament_service.find_departament_by_id(db, event.departament_id) is None:
            raise ValueError("Departament not found")

        event = self.__repository.create(
            db,
            name=event.name,
            event_datetime=event.datetime,
            departament_id=event.departament_id
        )

        return self.get_event_read(event)

    def add_user_to_event(self, db: Session, user_id: int, event_id: int) -> EventRead:
        userRepository = UserRepository()

        user = userRepository.find_by_id(db, user_id)
        if user is None:
            raise ValueError("User not found")
        event = self.__repository.get_event_by_id(db, event_id)
        if event is None:
            raise ValueError("Event not found")

        if len(event.users) >= 5:
            raise ValueError("Too many users")

        for user_event in user.events:
            if user_event.event_id == event_id:
                raise ValueError("Event already registered")
            if user_event.datetime == event.datetime:
                raise ValueError("User already registered in this time")

        event = self.__repository.add_event_user(db, user_id, event_id)
        return self.get_event_read(event)

    def get_events_by_user(self, db: Session, user_id: int) -> List[EventRead]:
        rep = []
        for event in self.__repository.get_events_by_user_id(db, user_id):
            rep.append(self.get_event_read(event))
        return rep

    def find_event_by_id(self, db: Session, event_id: int) -> EventModel:
        return self.__repository.get_event_by_id(db, event_id)

    def get_all(self, db: Session) -> list[EventRead]:
        events = self.__repository.get_all(db)
        rep = []
        for event in events:
            rep.append(self.get_event_read(event))
        return rep
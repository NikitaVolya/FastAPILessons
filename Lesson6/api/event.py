from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from repositories.events import EventRepository
from schemas.event import EventRead, EventCreate
from services.events import EventService

event_router = APIRouter(prefix="/events", tags=["events"])



@event_router.post("/create", response_model=EventRead)
async def create_event(
        event: EventCreate,
        db: Session = Depends(get_db)):
    service = EventService(EventRepository())
    try:
        return service.register(db, event)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@event_router.post("{event_id}/user/{user_id}", response_model=EventRead)
async def add_event_user(
        event_id: int,
        user_id: int,
        db: Session = Depends(get_db)):
    service = EventService(EventRepository())
    try:
        return service.add_user_to_event(db, event_id, user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@event_router.get("/user/{user_id}", response_model=List[EventRead])
async def get_event_user(
        user_id: int,
        db: Session = Depends(get_db)
):
    service = EventService(EventRepository())
    try:
        return service.get_events_by_user(db, user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@event_router.get("", response_model=list[EventRead])
async def read_events(db: Session = Depends(get_db)):
    service = EventService(EventRepository())
    return service.get_all(db)
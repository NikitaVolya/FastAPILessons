from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.session import get_db
from repositories.events import EventRepository
from schemas.event import EventRead
from schemas.user import UserCreate, UserRead
from services.events import EventService
from services.users import UserService
from repositories.users import UserRepository


user_router = APIRouter(prefix="/users", tags=["users"])



@user_router.post("/register", response_model=UserRead)
async def register_user(
        user: UserCreate,
        db: Session = Depends(get_db),
):
    service = UserService(UserRepository())
    try:
        user = service.register(db, user)
        return UserRead(id=user.id, first_name=user.first_name, last_name=user.last_name, role_name=user.role.name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@user_router.get("", response_model=List[UserRead])
async def get_users(db: Session = Depends(get_db)):
    service = UserService(UserRepository())
    return service.get_all(db)
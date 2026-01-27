from fastapi import FastAPI

from api.departament import departament_router
from api.event import event_router
from api.role import role_router
from api.user import user_router
from db.session import engine
from models.user import Base

app = FastAPI(
    title="FastAPI Lesson 6",
    description="FastAPI Lesson 6, Postgres SQL",
    version="1.0.0",
)

Base.metadata.create_all(engine)

app.include_router(role_router)
app.include_router(departament_router)
app.include_router(user_router)
app.include_router(event_router)
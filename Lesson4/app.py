from fastapi import FastAPI

from routes.match import match_router
from routes.player import player_router
from routes.tournament import tournament_router

app = FastAPI(
    title="FastAPI Lesson 3",
    description="FastAPI Lesson 3, Put and Patch",
    version="1.0.0",
)


app.include_router(tournament_router)
app.include_router(player_router)
app.include_router(match_router)
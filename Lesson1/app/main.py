from fastapi import FastAPI
from app.routers import exercices

app = FastAPI()

app.include_router(exercices.router)


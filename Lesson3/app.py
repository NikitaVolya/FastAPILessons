from fastapi import FastAPI
from routes import books

app = FastAPI(
    title="FastAPI Lesson 3",
    description="FastAPI Lesson 3, Put and Patch",
    version="1.0.0",
)

app.include_router(books.router)
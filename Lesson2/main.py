from fastapi import FastAPI
from routers import users, products

app = FastAPI(
    title="FastAPI Lesson 2",
    description="FastAPI Lesson 2, Pydanti",
    version="1.0.0",
)

app.include_router(users.router)
app.include_router(products.router)

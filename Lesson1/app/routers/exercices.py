from typing import Optional
from fastapi import APIRouter


router = APIRouter(prefix="/exercices", tags=["Exercices"])

@router.get("/hello")
async def hello():
    return {"message": "Hello World"}

@router.get("/square/{number}")
async def square(number: int):
    return {
        "number": number,
        "square": number * number,
    }

@router.get("/greet")
async def greet(name: str = "Name", age: Optional[int] = None):
    return {
        "message": f"Hello, {name}!",
        "age": age,
    }

@router.get("/items/{item_id}")
async def search(item_id: int, q: Optional[str] = None):
    return {
        "item_id": item_id,
        "q": q,
    }

@router.get("/calc")
async def calc(a: int, b: int):
    return {
        "a": a,
        "b": b,
        "sum": a + b,
        "diff": a - b,
        "prod": a * b,
        "div": (a / b if b != 0 else "undefined"),
    }
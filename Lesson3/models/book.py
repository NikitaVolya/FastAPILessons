from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, Field


class BookModel(BaseModel):
    id: int
    title: str = Field(min_length=3, max_length=100)
    author: str = Field(min_length=3, max_length=50)
    description: Optional[str] = Field(max_length=500)
    year: Optional[int] = Field(ge=1450)
    rating: Optional[Decimal] = Field(ge=0, le=5, max_digits=2)
    tags: Optional[str] = ""
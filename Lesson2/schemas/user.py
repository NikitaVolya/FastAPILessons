from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    age: int = Field(ge=14)
    is_active: bool = Field(default=True)


class UserResponse(BaseModel):
    id: int = 1
    email: EmailStr
    age: int
    is_active: bool

    class Config:
        from_attributes = True
        response_model_exclude_none = True


class FeedbackMessage(BaseModel):
    name: str = Field(min_length=2)
    email: EmailStr
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = Field(max_length=200)

class FeedbackResponse(BaseModel):
    name: str = Field(min_length=2)
    email: EmailStr
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = Field(max_length=200)
    message: str = "Thank you for your feedback!"

    class Config:
        from_attributes = True
        response_model_exclude_none = True
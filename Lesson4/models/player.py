from pydantic import BaseModel, Field, EmailStr


class PlayerModel(BaseModel):
    id: int
    name: str = Field(min_length=3, max_length=50)
    email: str = EmailStr()
    score: float = Field(ge=0)
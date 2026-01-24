from typing import Optional

from pydantic import BaseModel, Field, EmailStr

from models.player import PlayerModel


class PlayerCreate(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    email: str = EmailStr()
    score: float = Field(ge=0)


class PlayerUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    score: Optional[float] = Field(default=None, ge=0)

class PlayerStatistics(PlayerModel):
    tournament_score: float = Field(ge=0)
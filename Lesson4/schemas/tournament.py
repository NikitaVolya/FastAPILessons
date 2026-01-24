from typing import Optional

from pydantic import BaseModel, Field
from datetime import datetime
from models.player import PlayerModel
from models.match import MatchModel


class TournamentCreate(BaseModel):
    name: str = Field(min_length=5, max_length=100)
    game: str
    date: datetime
    max_players: int = Field(ge=5, le=100)

class TournamentUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=5, max_length=100)
    game: Optional[str] = Field(default=None)
    date: Optional[datetime] = Field(default=None)
    max_players: Optional[int] = Field(default=None, ge=5, le=100)

class CompleteTournament(TournamentCreate):
    id: int
    players: list[PlayerModel] = list()
    matches: list[MatchModel] = list()
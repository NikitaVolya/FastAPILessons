from typing import Optional

from pydantic import BaseModel, Field
from datetime import datetime



class TournamentModel(BaseModel):
    id: int
    name: str = Field(min_length=5, max_length=100)
    game: str
    date: datetime
    max_players: int = Field(ge=5, le=100)
    player_ids: Optional[list[int]] = list()
    match_ids: Optional[list[int]] = list()

    class Config:
        from_attributes = True
        response_model_exclude_none = True
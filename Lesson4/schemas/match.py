from pydantic import BaseModel, Field


class MatchCreate(BaseModel):
    tournament_id: int
    player1_id: int
    player2_id: int
    player1_score: float = Field(ge=0)
    player2_score: float = Field(ge=0)
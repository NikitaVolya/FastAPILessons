from fastapi import APIRouter, HTTPException

from models.match import MatchModel
from schemas.match import MatchCreate
from services.pseudo_db import PseudoDB

match_router = APIRouter()


@match_router.post("/matches", response_model=MatchModel)
async def create_match(match: MatchCreate):

    if await PseudoDB.first_tournament(lambda t: t.id == match.tournament_id) is None:
        raise HTTPException(status_code=404, detail="Match not found")

    rep = await PseudoDB.create_match(match)
    return rep

@match_router.get("/tournaments/{tournament_id}/matches", response_model=list[MatchModel])
async def get_tournaments(tournament_id: int):

    tournament = await PseudoDB.first_tournament(lambda t: t.id == tournament_id)
    if tournament is None:
        raise HTTPException(status_code=404, detail="Tournament not found")

    matches = await tournament.get_matches(lambda m: m.tournament_id == tournament_id)
    return matches
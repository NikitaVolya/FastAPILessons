from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from models.player import PlayerModel
from schemas.player import PlayerCreate, PlayerUpdate
from services.pseudo_db import PseudoDB

player_router = APIRouter()


@player_router.post("/players/", response_model=PlayerModel)
async def create_players(players_data: PlayerCreate):

    player = await PseudoDB.create_player(players_data)
    return player


@player_router.get("/players/")
async def get_all_players(min_score: Optional[int] = Query(None, ge=0),
                          name: Optional[str] = Query(None)):

    if min_score is None and name is None:
        rep = await PseudoDB.get_players()
    else:
        rep = await PseudoDB.get_players(
            lambda p:
            (min_score is None or p.score >= min_score) and
            (name is None or name.lower() in p.name.lower())
        )

    return rep

@player_router.get("/players/{player_id}")
async def get_player_by_id(player_id: int):

    rep = await PseudoDB.first_player(lambda p: p.id == player_id)
    if rep is None:
        raise HTTPException(status_code=404, detail="Player not found")

    return rep

@player_router.patch("/players/{player_id}")
async def update_player_by_id(player_id: int, data: PlayerUpdate):

    player = await PseudoDB.first_player(lambda p: p.id == player_id)
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    player = player.copy(update=data.dict(exclude_unset=True))

    rep = await PseudoDB.update_player(player)
    if rep is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return rep

@player_router.delete("/players/{player_id}")
async def delete_player_by_id(player_id: int):
    player = await PseudoDB.first_player(lambda p: p.id == player_id)
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    await PseudoDB.remove_player(lambda p: p.id == player_id)
    return {"message": "Player deleted"}
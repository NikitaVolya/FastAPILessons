from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from watchfiles import awatch

from models.tournament import TournamentModel
from schemas.player import PlayerStatistics
from schemas.tournament import TournamentCreate, CompleteTournament, TournamentUpdate
from services.pseudo_db import PseudoDB

tournament_router = APIRouter()


@tournament_router.post("/tournaments", response_model=TournamentModel)
async def create_tournament(tournament_data: TournamentCreate):
    tournament_model = await PseudoDB.create_tournament(tournament_data)
    return tournament_model

@tournament_router.get("/tournaments")
async def get_tournaments(game: Optional[str] = Query(None)) -> list[TournamentModel]:

    if game is None:
        tournaments = await PseudoDB.get_tournaments()
    else:
        tournaments = await PseudoDB.get_tournaments(lambda p: p.game.lower() == game.lower())

    return tournaments

@tournament_router.get("/tournaments/{tournament_id}", response_model=CompleteTournament)
async def get_tournament(tournament_id: int):

    tournament = await PseudoDB.first_tournament(lambda t: t.id == tournament_id)
    tournament = CompleteTournament(**tournament.dict())

    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")

    tournament = await PseudoDB.tournament_include_match(tournament)
    tournament = await PseudoDB.tournament_include_player(tournament)
    return tournament

@tournament_router.patch("/tournaments/{tournament_id}", response_model=TournamentModel)
async def update_tournament(tournament_id: int, tournament_data: TournamentUpdate):

    tournament = await PseudoDB.first_tournament(lambda t: t.id == tournament_id)

    if tournament is None:
        raise HTTPException(status_code=404, detail="Tournament not found")

    updated_tournament = tournament.copy(update=tournament_data.dict(exclude_unset=True))

    rep_tournament = await PseudoDB.update_tournament(updated_tournament)
    return rep_tournament

@tournament_router.delete("/tournaments/{tournament_id}")
async def delete_tournament(tournament_id: int):

    rep = await PseudoDB.remove_tournament(lambda t: t.id == tournament_id)

    if rep is None:
        raise HTTPException(status_code=404, detail="Tournament not found")
    else:
        return {"message": f"Tournament {tournament_id} deleted"}

@tournament_router.post("/tournaments/{tournament_id}/players/{player_id}", response_model=TournamentModel)
async def add_player_to_tournament(player_id: int, tournament_id: int):

    tournament = await PseudoDB.first_tournament(lambda t: t.id == tournament_id)
    if tournament is None:
        raise HTTPException(status_code=404, detail="Tournament not found")

    player = await PseudoDB.first_player(lambda p: p.id == player_id)
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")

    if len(tournament.player_ids) == tournament.max_players:
        raise HTTPException(status_code=400, detail="Tournament already full")

    if player.id in tournament.player_ids:
        raise HTTPException(status_code=400, detail="Player already on tournament")

    tournament.player_ids.append(player_id)
    rep = await PseudoDB.update_tournament(tournament)
    return rep

@tournament_router.delete("/tournaments/{tournament_id}/players/{player_id}")
async def remove_player_from_tournament(player_id: int, tournament_id: int):
    tournament = await PseudoDB.first_tournament(lambda t: t.id == tournament_id)
    if tournament is None:
        raise HTTPException(status_code=404, detail="Tournament not found")

    player = await PseudoDB.first_player(lambda p: p.id == player_id)
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")

    if player.id not in tournament.player_ids:
        raise HTTPException(status_code=400, detail="Player is not on tournament")

    tournament.player_ids.remove(player_id)
    rep = await PseudoDB.update_tournament(tournament)
    return rep

@tournament_router.get("/tournaments/{tournament_id}/standings/")
async def get_tournament_standings(tournament_id: int):
    rep: dict[int, PlayerStatistics] = dict()

    for match in await PseudoDB.get_matches(lambda m: m.tournament_id == tournament_id):

        # Player 1 score add to dict
        if match.player1_id not in rep:
            player = await PseudoDB.first_player(lambda p: p.id == match.player1_id)
            rep[match.player1_id] = PlayerStatistics(
                **player.dict(),
                tournament_score=0
            )
        rep[match.player1_id].tournament_score += match.player1_score

        # Player 2 score add to dict
        if match.player2_id not in rep:
            player = await PseudoDB.first_player(lambda p: p.id == match.player2_id)
            rep[match.player2_id] = PlayerStatistics(
                **player.dict(),
                tournament_score=0
            )
        rep[match.player2_id].tournament_score += match.player2_score

    rep = list(rep.values())
    rep = sorted(rep, key=lambda p: p.tournament_score, reverse=True)
    return rep
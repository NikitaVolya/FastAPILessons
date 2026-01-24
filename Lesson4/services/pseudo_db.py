from typing import Callable

from schemas.match import MatchCreate
from schemas.player import PlayerUpdate
from schemas.tournament import TournamentCreate, CompleteTournament, TournamentUpdate
from models.tournament import TournamentModel
from models.player import PlayerModel
from models.match import MatchModel


class PseudoDB:

    __tournamentId = 0
    __playerId = 0
    __matchId = 0

    __tournaments: list[TournamentModel] = list()
    __players: list[PlayerModel] = list()
    __matches: list[MatchModel] = list()

    @staticmethod
    async def create_tournament(tournament: TournamentCreate) -> TournamentModel:

        new_tournament = TournamentModel(
                id=PseudoDB.__tournamentId,
                **tournament.dict()
            )

        PseudoDB.__tournaments.append(new_tournament)
        PseudoDB.__tournamentId += 1

        return new_tournament


    @staticmethod
    async def create_player(player: TournamentCreate) -> TournamentModel:

        new_player = PlayerModel(
            id=PseudoDB.__playerId,
            **player.dict()
        )

        PseudoDB.__players.append(new_player)
        PseudoDB.__playerId += 1

        return new_player

    @staticmethod
    async def create_match(match: MatchCreate) -> MatchModel | None:

        if await PseudoDB.first_tournament(lambda t: t.id == match.tournament_id) is None:
            return None

        winner_id = match.player1_id if match.player1_score > match.player2_score else match.player2_id

        new_match = MatchModel(
            id=PseudoDB.__matchId,
            winner_id=winner_id,
            **match.dict()
        )

        PseudoDB.__matches.append(new_match)
        PseudoDB.__matchId += 1

        player1 = await PseudoDB.first_player(lambda p: p.id == match.player1_id)
        player1.score += match.player1_score
        await PseudoDB.update_player(player1)

        player2 = await PseudoDB.first_player(lambda p: p.id == match.player2_id)
        player2.score += match.player2_score
        await PseudoDB.update_player(player2)

        return new_match

    @staticmethod
    async def first_tournament(predicate: Callable[[TournamentModel], bool], default = None) -> TournamentModel:
        for tournament in PseudoDB.__tournaments:
            if predicate(tournament):
                return tournament
        return default

    @staticmethod
    async def first_player(predicate: Callable[[PlayerModel], bool], default = None) -> PlayerModel:
        for player in PseudoDB.__players:
            if predicate(player):
                return player
        return default

    @staticmethod
    async def first_match(predicate: Callable[[MatchModel], bool], default = None) -> MatchModel:
        for match in PseudoDB.__matches:
            if predicate(match):
                return match
        return default

    @staticmethod
    async def get_tournaments(predicate: Callable[[TournamentModel], bool] = None) -> list[TournamentModel]:
        rep = []
        for tournament in PseudoDB.__tournaments:
            if predicate is None or predicate(tournament):
                rep.append(tournament)
        return rep

    @staticmethod
    async def get_matches(predicate: Callable[[MatchModel], bool] = None) -> list[MatchModel]:
        rep = []
        for match in PseudoDB.__matches:
            if predicate is None or predicate(match):
                rep.append(match)
        return rep

    @staticmethod
    async def get_players(predicate: Callable[[PlayerModel], bool] = None) -> list[PlayerModel]:
        rep = []
        for player in PseudoDB.__players:
            if predicate is None or predicate(player):
                rep.append(player)
        return rep

    @staticmethod
    async def tournament_include_player(tournament: CompleteTournament) -> TournamentModel:
        tournament_data = await PseudoDB.first_tournament(lambda t: t.id == tournament.id)

        tournament.players = []
        for player in PseudoDB.__players:
            if player.id in tournament_data.player_ids:
                tournament.players.append(player)
        return tournament

    @staticmethod
    async def tournament_include_match(tournament: CompleteTournament) -> TournamentModel:
        tournament_data = await PseudoDB.first_tournament(lambda t: t.id == tournament.id)

        tournament.matches = []
        for match in PseudoDB.__matches:
            if match.id in tournament_data.match_ids:
                tournament.matches.append(match)
        return tournament

    @staticmethod
    async def update_tournament(tournament: TournamentModel) -> TournamentModel | None:

        index = -1
        for i in range(0, len(PseudoDB.__tournaments)):
            if PseudoDB.__tournaments[i].id == tournament.id:
                index = i
                break

        if index == -1:
            return None

        PseudoDB.__tournaments[index] = tournament
        return PseudoDB.__tournaments[-1]

    @staticmethod
    async def remove_tournament(predicate: Callable[[TournamentModel], bool] = None) -> TournamentModel | None:
        for tournament in PseudoDB.__tournaments:
            if predicate is None or predicate(tournament):
                PseudoDB.__tournaments.remove(tournament)
                return tournament
        return None

    @staticmethod
    async def update_player(player: PlayerModel) -> PlayerModel | None:

        index = -1
        for i in range(0, len(PseudoDB.__players)):
            if PseudoDB.__players[i].id == player.id:
                index = i
                break

        if index == -1:
            return None

        PseudoDB.__players[index] = player
        return PseudoDB.__players[-1]

    @staticmethod
    async def remove_player(predicate: Callable[[PlayerModel], bool] = None) -> PlayerModel | None:
        for player in PseudoDB.__players:
            if predicate is None or predicate(player):
                PseudoDB.__players.remove(player)
                return player
        return None
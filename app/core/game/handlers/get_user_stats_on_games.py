from app.core.common.handler import Handler
from app.core.game.exceptions import PlayerNotFoundException
from app.core.game import dto
from app.core.game.protocols import PlayerGateway


class GetUserStatsOnGamesByTgIdHandler(Handler):
    def __init__(
        self,
        player_gateway: PlayerGateway,
    ):
        self._player_gateway = player_gateway

    async def execute(self, user_tg_id: int) -> dto.UserStats:
        players = await self._player_gateway.get_players_by_user_tg_id(
            user_tg_id
        )

        if not players:
            raise PlayerNotFoundException

        games_results = [
            dto.PlayerStats(
                state=player.status,
                score=player.score,
                bet=player.bet,
            )
            for player in players
        ]
        user_stats = dto.UserStats(
            games_results=games_results,
        )

        return user_stats

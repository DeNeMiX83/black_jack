from uuid import UUID
from app.core.common.handler import Handler
from app.core.game.protocols import PlayerGateway
from app.core.game import entities as game_entities


class GetGamePlayersHandler(Handler):
    def __init__(
        self,
        player_gateway: PlayerGateway,
    ):
        self._player_gateway = player_gateway

    async def execute(self, game_id: UUID) -> list[game_entities.Player]:
        players = await self._player_gateway.get_players_by_game_id(game_id)
        return players

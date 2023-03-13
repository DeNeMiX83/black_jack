from uuid import UUID
from app.core.common.handler import Handler
from app.core.game.protocols import PlayerGateway
from app.core.game import entities as game_entities


class GetPlayerHandler(Handler):
    def __init__(
        self,
        player_gateway: PlayerGateway,
    ):
        self._player_gateway = player_gateway

    async def execute(self, player_id: UUID) -> game_entities.Player:
        player = await self._player_gateway.get(player_id)

        return player

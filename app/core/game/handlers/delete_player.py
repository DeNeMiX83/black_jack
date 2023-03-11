from uuid import UUID
from app.core.common.protocols import Commiter
from app.core.common.handler import Handler
from app.core.game.protocols import PlayerGateway
from app.core.game import entities as game_entities


class DeletePlayerHandler(Handler):
    def __init__(
        self,
        player_gateway: PlayerGateway,
        commiter: Commiter
    ):
        self._player_gateway = player_gateway
        self._commiter = commiter

    async def execute(self, player_id: UUID) -> None:
        await self._player_gateway.delete_by_id(player_id)

        await self._commiter.commit()




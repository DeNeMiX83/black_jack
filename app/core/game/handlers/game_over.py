from uuid import UUID
from app.core.common.handler import Handler
from app.core.common.protocols import Commiter
from app.core.game.protocols import GameGateway


class GameOverHandler(Handler):
    def __init__(
        self,
        game_gateway: GameGateway,
        commiter: Commiter,
    ):
        self._game_gateway = game_gateway
        self._commiter = commiter

    async def execute(self, game_id: UUID) -> None:
        game = await self._game_gateway.get(game_id)
        game.is_over = True

        await self._commiter.commit()

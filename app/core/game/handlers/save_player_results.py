from app.core.common.handler import Handler
from app.core.common.protocols import Commiter
from app.core.game.protocols import (
    PlayerGateway,
)
from app.core.game import dto


class SavePlayerResultsHandler(Handler):
    def __init__(
        self,
        player_gateway: PlayerGateway,
        commiter: Commiter,
    ):
        self._player_gateway = player_gateway
        self._commiter = commiter

    async def execute(self, results: list[dto.PlayerResult]) -> None:
        for result in results:
            player = await self._player_gateway.get(
                result.player_id, for_update=True
            )
            player.status = result.new_state
            player.user.balance += result.winning

        await self._commiter.commit()

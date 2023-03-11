from app.core.common.handler import Handler
from app.core.common.protocols import Commiter
from app.core.game.protocols import (
    PlayerGateway,
)
from app.core.game import dto


class UpdatePlayerStateHandler(Handler):
    def __init__(
        self,
        player_gateway: PlayerGateway,
        commiter: Commiter,
    ):
        self._player_gateway = player_gateway
        self._commiter = commiter

    async def execute(self, state: dto.PlayerStateUpdate) -> None:
        player = await self._player_gateway.get(state.player_id)

        player.status = state.new_state

        await self._commiter.commit()

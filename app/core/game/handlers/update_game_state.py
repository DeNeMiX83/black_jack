from app.core.common.handler import Handler
from app.core.common.protocols import Commiter
from app.core.game.protocols import (
    GameGateway, GameStateGateway
)
from app.core.chat.protocols import ChatGateway
from app.core.game import dto as game_dto


class UpdateGameStateHandler(Handler):
    def __init__(
        self,
        game_state_gateway: GameStateGateway,
        commiter: Commiter,
    ):
        self._game_state_gateway = game_state_gateway
        self._commiter = commiter

    async def execute(self, game_state: game_dto.GameStateUpdate) -> None:
        game_state_entity = await self._game_state_gateway.get_by_game_id(
            game_state.game_id  # type: ignore
        )

        game_state_entity.state = game_state.new_state

        await self._commiter.commit()

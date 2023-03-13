from uuid import UUID
from app.core.common.handler import Handler
from app.core.game.protocols import GameStateGateway
from app.core.game import entities as game_entities


class GetGameStateHandler(Handler):
    def __init__(
        self,
        game_state_gateway: GameStateGateway,
    ):
        self._game_state_gateway = game_state_gateway

    async def execute(self, game_id: UUID) -> game_entities.GameState:
        game_state_entity = (
            await self._game_state_gateway.get_by_game_id(game_id)  # type: ignore
        )
        return game_state_entity

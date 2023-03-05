from typing import Protocol
from app.core.game import entities


class GameStateGateway(Protocol):
    async def create(
        self, game_state: entities.GameState
    ) -> None:
        raise NotImplementedError

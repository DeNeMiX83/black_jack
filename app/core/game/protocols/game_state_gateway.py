from typing import Protocol
from uuid import UUID
from app.core.game import entities


class GameStateGateway(Protocol):
    async def get_by_game_id(self, game_id: UUID) -> entities.GameState:
        raise NotImplementedError

    async def create(
        self, game_state: entities.GameState
    ) -> None:
        raise NotImplementedError
    
    async def update(self, game_state: entities.GameState) -> None:
        raise NotImplementedError

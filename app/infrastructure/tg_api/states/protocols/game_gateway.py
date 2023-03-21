from typing import Protocol, Optional
from ..dto import GameStateData, GameStateKey


class GameStateGateway(Protocol):
    async def create(self, key: GameStateKey, data: GameStateData):
        raise NotImplementedError

    async def get(self, key: GameStateKey) -> Optional[GameStateData]:
        raise NotImplementedError

    async def delete(self, key: GameStateKey) -> None:
        raise NotImplementedError

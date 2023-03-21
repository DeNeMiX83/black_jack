from typing import Protocol, Optional
from ..dto import PlayerStateData, PlayerStateKey


class PlayerStateGateway(Protocol):
    async def create(self, key: PlayerStateKey, data: PlayerStateData):
        raise NotImplementedError

    async def get(self, key: PlayerStateKey) -> Optional[PlayerStateData]:
        raise NotImplementedError

    async def delete(self, key: PlayerStateKey) -> None:
        raise NotImplementedError

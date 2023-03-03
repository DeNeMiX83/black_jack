from typing import Protocol
from app.core.player import entities


class PlayerGateway(Protocol):
    async def create(self, player: entities.Player) -> None:
        raise NotImplementedError

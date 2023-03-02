from typing import Protocol
from app.core.player.entities import Player


class PlayerGateway(Protocol):
    async def create(self, player: Player) -> Player:
        raise NotImplementedError

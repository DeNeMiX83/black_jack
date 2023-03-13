from typing import Protocol
from uuid import UUID
from app.core.game import entities


class PlayerCardsGateway(Protocol):
    async def create(self, player: entities.PlayerCard) -> None:
        raise NotImplementedError

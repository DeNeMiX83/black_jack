from typing import Protocol
from uuid import UUID
from app.core.game.entities import Game


class GameGateway(Protocol):
    async def get_by_chat_id(self, chat_id: UUID) -> Game:
        raise NotImplementedError

    async def create(self, game: Game) -> None:
        raise NotImplementedError

    async def update(self, game: Game) -> None:
        raise NotImplementedError

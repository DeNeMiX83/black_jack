from typing import Protocol
from app.core.game.entities import Game


class GameGateway(Protocol):
    async def create(self, game: Game) -> None:
        raise NotImplementedError

    async def update(self, game: Game) -> Game:
        raise NotImplementedError

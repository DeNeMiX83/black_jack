from app.core.game.protocols import GameGateway
from app.infrastructure.store.sqlalchemy.gateway import BaseGateway
from app.core.game import entities


class GameGatewayImpl(BaseGateway, GameGateway):
    async def create(self, game: entities.Game) -> None:
        self._session.add(game)

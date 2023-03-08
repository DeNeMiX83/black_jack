from sqlalchemy.exc import IntegrityError
from app.infrastructure.store.sqlalchemy.gateway import BaseGateway
from app.core.common.exceptions import GatewayException
from app.core.game.protocols import GameGateway
from app.core.game import entities


class GameGatewayImpl(BaseGateway, GameGateway):
    async def create(self, game: entities.Game) -> None:
        self._session.add(game)
        try:
            await self._session.flush()
        except IntegrityError as e:
            await self._session.rollback()
            raise GatewayException(e)

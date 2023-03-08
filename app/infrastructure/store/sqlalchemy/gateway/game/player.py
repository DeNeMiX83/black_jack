from sqlalchemy.exc import IntegrityError
from app.infrastructure.store.sqlalchemy.gateway import BaseGateway
from app.core.common.exceptions import GatewayException
from app.core.game.protocols import PlayerGateway
from app.core.game import entities


class PlayerGatewayImpl(BaseGateway, PlayerGateway):
    async def create(self, player: entities.Player) -> None:
        self._session.add(player)
        try:
            await self._session.flush()
        except IntegrityError as e:
            await self._session.rollback()
            raise GatewayException(e)

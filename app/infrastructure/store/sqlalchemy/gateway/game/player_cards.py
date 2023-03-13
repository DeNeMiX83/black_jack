from sqlalchemy.exc import IntegrityError
from app.infrastructure.store.sqlalchemy.gateway import BaseGateway
from app.core.common.exceptions import GatewayException
from app.core.game.protocols import PlayerCardsGateway
from app.core.game import entities


class PlayerCardsGatewayImpl(BaseGateway, PlayerCardsGateway):
    async def create(self, player_card: entities.PlayerCard) -> None:
        self._session.add(player_card)
        try:
            await self._session.flush()
        except IntegrityError as e:
            await self._session.rollback()
            raise GatewayException(e)

from typing import Optional
from uuid import UUID
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, and_
from app.infrastructure.store.sqlalchemy.gateway import BaseGateway
from app.core.common.exceptions import GatewayException
from app.core.game.protocols import GameGateway
from app.core.game import entities


class GameGatewayImpl(BaseGateway, GameGateway):
    async def get(self, id: UUID) -> entities.Game:
        return await self._session.get(entities.Game, id)

    async def get_by_chat_id(self, chat_id: UUID) -> entities.Game:
        stmt = select(entities.Game).where(
            and_(
                entities.Game.chat_id == chat_id, entities.Game.is_over == False
            )
        )
        result = await self._session.execute(stmt)
        return result.scalars().first()

    async def create(self, game: entities.Game) -> None:
        self._session.add(game)
        try:
            await self._session.flush()
        except IntegrityError as e:
            await self._session.rollback()
            raise GatewayException(e)

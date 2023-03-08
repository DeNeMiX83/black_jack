from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from app.infrastructure.store.sqlalchemy.gateway import BaseGateway
from app.core.common.exceptions import GatewayException
from app.core.chat.protocols import ChatGateway
from app.core.chat import entities


class ChatGatewayImpl(BaseGateway, ChatGateway):
    async def create(self, chat: entities.Chat) -> None:
        self._session.add(chat)
        try:
            await self._session.flush()
        except IntegrityError as e:
            await self._session.rollback()
            raise GatewayException(e)

    async def get_by_tg_id(self, tg_id: int) -> entities.Chat:
        stmt = select(entities.Chat).where(entities.Chat.tg_id == tg_id)
        result = await self._session.execute(stmt)
        return result.scalars().first()

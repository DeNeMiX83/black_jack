from sqlalchemy import select
from app.core.chat.protocols import ChatGateway
from app.infrastructure.store.sqlalchemy.gateway import BaseGateway
from app.core.chat import entities


class ChatGatewayImpl(BaseGateway, ChatGateway):
    async def create(self, chat: entities.Chat) -> None:
        print(self._session, 3412342314123423)
        self._session.add(chat)
        print('453214123431242134')

    async def get_by_tg_id(self, tg_id: int) -> entities.Chat:
        stmt = select(entities.Chat).where(entities.Chat.tg_id == tg_id)
        result = await self._session.execute(stmt)
        return result.scalars().first()

from typing import Protocol
from app.core.chat.entities import Chat


class ChatGateway(Protocol):
    async def get_by_tg_id(self, tg_id: int) -> Chat:
        raise NotImplementedError

    async def create(self, chat: Chat) -> None:
        raise NotImplementedError

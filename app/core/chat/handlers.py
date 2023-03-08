from app.core.common.handler import Handler
from app.core.common.protocols import Commiter
from app.core.chat.protocols import ChatGateway
from app.core.chat import dto as chat_dto
from app.core.chat import entities as chat_entities


class CreateChatHandler(Handler):
    def __init__(
        self,
        chat_gateway: ChatGateway,
        commiter: Commiter,
    ):
        self._chat_gateway = chat_gateway
        self._commiter = commiter

    async def execute(self, chat: chat_dto.ChatCreate) -> None:
        chat_entity = chat_entities.Chat(
            tg_id=chat.tg_id,
            name=chat.name,
        )
        await self._chat_gateway.create(chat_entity)
        print('done add')

        await self._commiter.commit()

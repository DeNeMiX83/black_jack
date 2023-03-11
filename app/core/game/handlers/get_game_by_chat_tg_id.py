from app.core.common.handler import Handler
from app.core.game.protocols import GameGateway
from app.core.chat.protocols import ChatGateway
from app.core.chat import dto as chat_dto
from app.core.game import entities as game_entities


class GetGameByChatTgIdHandler(Handler):
    def __init__(
        self,
        game_gateway: GameGateway,
        chat_gateway: ChatGateway,
    ):
        self._game_gateway = game_gateway
        self._chat_gateway = chat_gateway

    async def execute(self, chat: chat_dto.Chat) -> game_entities.Game:
        chat_entity = await self._chat_gateway.get_by_tg_id(chat.tg_id)
        game_entity = await self._game_gateway.get_by_chat_id(chat_entity.id)  # type: ignore

        return game_entity

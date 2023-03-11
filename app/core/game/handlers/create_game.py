from typing import Optional
from app.core.common.exceptions import GatewayException
from app.core.common.handler import Handler
from app.core.common.protocols import Commiter
from app.core.game.exceptions import (
    ChatNotFoundException, GameAlreadyExistsException
)
from app.core.game.protocols import (
    GameGateway, GameStateGateway
)
from app.core.chat.protocols import ChatGateway
from app.core.game import dto as game_dto
from app.core.game import entities as game_entities


class CreateAndReturnGameHandler(Handler):
    def __init__(
        self,
        game_gateway: GameGateway,
        game_state_gateway: GameStateGateway,
        chat_gateway: ChatGateway,
        commiter: Commiter,
    ):
        self._game_gateway = game_gateway
        self._game_state_gateway = game_state_gateway
        self._chat_gateway = chat_gateway
        self._commiter = commiter
        self._game: Optional[game_entities.Game] = None

    async def execute(self, game: game_dto.GameCreate) -> game_entities.Game:
        await self._create_game(game)
        await self._create_game_state()

        await self._commiter.commit()

        return self._game  # type: ignore

    async def _create_game(self, game: game_dto.GameCreate) -> None:
        chat = await self._chat_gateway.get_by_tg_id(game.chat_tg_id)
        if chat is None:
            raise ChatNotFoundException('Chat not found')

        self._game = game_entities.Game(chat=chat)

        try:
            await self._game_gateway.create(self._game)
        except GatewayException as e:
            raise GameAlreadyExistsException(e)

    async def _create_game_state(self) -> None:
        game_state = game_entities.GameState(
            game=self._game,  # type: ignore
        )
        await self._game_state_gateway.create(game_state)
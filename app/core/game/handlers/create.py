from app.core.common.handler import Handler
from app.core.common.protocols import Commiter
from app.core.game.protocols import GameGateway, GameStateGateway
from app.core.game.dto import GameCreate
from app.core.chat import entities as chat_entities
from app.core.game import entities as game_entities


class CreateGameHandler(Handler):
    def __init__(
        self,
        game_gateway: GameGateway,
        game_state_gateway: GameStateGateway,
        commiter: Commiter,
    ):
        self._game_gateway = game_gateway
        self._game_state_gateway = game_state_gateway
        self._commiter = commiter

    async def execute(self, game: GameCreate) -> None:
        new_game = await self._create_game(game)

        await self._create_game_state(new_game)

        await self._commiter.commit()

    async def _create_game(self, game: GameCreate) -> game_entities.Game:
        chat = chat_entities.Chat(
            tg_id=game.chat.tg_id,
            name=game.chat.name,
        )
        new_game = game_entities.Game(chat=chat, bet=game.bet)
        new_game = await self._game_gateway.create(new_game)

        return new_game

    async def _create_game_state(self, game):
        game_state = game_entities.GameState(
            game=game,
        )
        await self._game_state_gateway.create(game_state)

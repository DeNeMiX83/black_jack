from app.core.common.handler import Handler
from app.core.game.execprions import UserNotFoundException
from app.core.common.protocols import Commiter
from app.core.game.protocols import (
    GameGateway, GameStateGateway, PlayerGateway
)
from app.core.user.protocols import UserGateway
from app.core.chat.protocols import ChatGateway
from app.core.game import dto as chat_dto
from app.core.game import entities as game_entities
from app.core.user import entities as user_entities


class StartGameHandler(Handler):
    def __init__(
        self,
        game_gateway: GameGateway,
        game_state_gateway: GameStateGateway,
        player_gateway: PlayerGateway,
        user_gateway: UserGateway,
        chat_gateway: ChatGateway,
        commiter: Commiter,
    ):
        self._game_gateway = game_gateway
        self._game_state_gateway = game_state_gateway
        self._player_gateway = player_gateway
        self._user_gateway = user_gateway
        self._chat_gateway = chat_gateway
        self._commiter = commiter
        self.game

    async def execute(self, game: chat_dto.GameCreate) -> None:
        await self._create_game(game)
        await self._create_game_state(self.game)
        await self._add_players_to_game(game.players, self.game)

        await self._commiter.commit()

    async def _create_game(self, game: chat_dto.GameCreate) -> None:
        chat = await self._chat_gateway.get_by_tg_id(game.chat.tg_id)

        self.game = game_entities.Game(chat=chat)

        await self._game_gateway.create(self.game)

    async def _create_game_state(self, game: game_entities.Game) -> None:
        game_state = game_entities.GameState(
            game=game,
        )
        await self._game_state_gateway.create(game_state)

    async def _add_players_to_game(
        self, players: list[chat_dto.PlayerCreate], game: game_entities.Game
    ) -> None:
        for player in players:
            try:
                user = await self._user_gateway.get_by_tg_id(player.tg_id)
            except UserNotFoundException:
                user = user_entities.User(
                    tg_id=player.tg_id,
                    username=player.username,
                )
                await self._user_gateway.create(user)
            new_player = game_entities.Player(
                game=game,
                user=user,
            )
            await self._player_gateway.create(new_player)

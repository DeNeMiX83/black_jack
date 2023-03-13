from app.core.common.exceptions import GatewayException
from app.core.common.handler import Handler
from app.core.common.protocols import Commiter
from app.core.game.exceptions import PlayerAlreadyExistsException
from app.core.chat.protocols import ChatGateway
from app.core.game.protocols import (
    GameGateway, PlayerGateway
)
from app.core.user.protocols import UserGateway
from app.core.game import dto as game_dto
from app.core.game import entities as game_entities
from app.core.user import entities as user_entities


class AddPlayerHandler(Handler):
    def __init__(
        self,
        game_gateway: GameGateway,
        player_gateway: PlayerGateway,
        user_gateway: UserGateway,
        commiter: Commiter,
    ):
        self._game_gateway = game_gateway
        self._player_gateway = player_gateway
        self._user_gateway = user_gateway
        self._commiter = commiter

    async def execute(self, player: game_dto.PlayerCreate) -> None:
        user = await self._user_gateway.get_by_tg_id(player.tg_id)

        if user is None:
            user = user_entities.User(
                tg_id=player.tg_id,
                username=player.username,
                balance=1000,
            )
            await self._user_gateway.create(user)

        game = await self._game_gateway.get(player.game_id)

        new_player = game_entities.Player(
            game=game,
            user=user,
        )

        try:
            await self._player_gateway.create(new_player)
        except GatewayException as e:
            raise PlayerAlreadyExistsException(e)

        await self._commiter.commit()

from app.core.common.handler import Handler
from app.core.common.protocols import Commiter
from app.core.game.protocols import PlayerGateway, GameGateway
from app.core.game import dto as game_dto
from app.core.game.entities import player_status


class UpdatePlayerBetHandler(Handler):
    def __init__(
        self,
        player_gateway: PlayerGateway,
        commiter: Commiter,
    ):
        self._player_gateway = player_gateway
        self._commiter = commiter

    async def execute(self, bet: game_dto.Bet) -> None:
        current_game_player = await self._player_gateway.get(
            bet.player_id
        )
        
        if current_game_player.user.balance < bet.bet:
            raise ValueError

        current_game_player.bet = bet.bet
        current_game_player.status = player_status.PLAYING
        current_game_player.user.balance -= bet.bet

        await self._player_gateway.update(current_game_player)

        await self._commiter.commit()

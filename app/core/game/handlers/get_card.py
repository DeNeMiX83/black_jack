from random import choice
from uuid import UUID
from app.core.common.handler import Handler
from app.core.common.protocols import Commiter
from app.core.game.protocols import PlayerGateway, PlayerCardsGateway
from app.core.game import entities as game_entities


class GetCardHandler(Handler):
    def __init__(
        self,
        player_gateway: PlayerGateway,
        player_cards_gateway: PlayerCardsGateway,
        commiter: Commiter
    ):
        self._player_gateway = player_gateway
        self._player_cards_gateway = player_cards_gateway
        self._commiter = commiter

    async def execute(self, player_id: UUID) -> game_entities.Card:
        cards = (
            "1", "2", "3", "4", "5",
            "6", "7", "8", "9", "10",
            "J", "Q", "K", "A",
        )
        rank = choice(cards)
        card = game_entities.Card(rank)

        player = await self._player_gateway.get(player_id, for_update=True)
        player_card = game_entities.PlayerCard(
            player=player,
            card=card
        )

        await self._player_cards_gateway.create(player_card)
        player.score += card.weight

        await self._commiter.commit()

        return card
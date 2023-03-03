from app.core.game.protocols import PlayerGateway
from app.infrastructure.store.sqlalchemy.gateway import BaseGateway
from app.core.game import entities


class PlayerGatewayImpl(BaseGateway, PlayerGateway):
    async def create(self, player: entities.Player) -> None:
        self.session.add(player)

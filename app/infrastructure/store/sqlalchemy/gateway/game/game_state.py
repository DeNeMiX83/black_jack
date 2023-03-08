from app.core.game.protocols import GameStateGateway
from app.infrastructure.store.sqlalchemy.gateway import BaseGateway
from app.core.game import entities


class GameStateGatewayImpl(BaseGateway, GameStateGateway):
    async def create(self, game_state: entities.GameState) -> None:
        self._session.add(game_state)

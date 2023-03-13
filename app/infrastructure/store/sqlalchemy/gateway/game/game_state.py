from sqlalchemy import select
from uuid import UUID
from app.core.game.protocols import GameStateGateway
from app.infrastructure.store.sqlalchemy.gateway import BaseGateway
from app.core.game import entities


class GameStateGatewayImpl(BaseGateway, GameStateGateway):
    async def get_by_game_id(self, game_id: UUID, for_update=False) -> entities.GameState:
        stmt = select(entities.GameState).where(
            entities.GameState.game_id == game_id
        )
        if for_update:
            stmt = stmt.await_for_update()
        result = await self._session.execute(stmt)
        return result.scalars().first()

    async def create(self, game_state: entities.GameState) -> None:
        self._session.add(game_state)

from sqlalchemy import select, update
from uuid import UUID
from app.core.game.protocols import GameStateGateway
from app.infrastructure.store.sqlalchemy.gateway import BaseGateway
from app.core.game import entities


class GameStateGatewayImpl(BaseGateway, GameStateGateway):
    async def get_by_game_id(self, game_id: UUID) -> entities.GameState:
        stmt = select(entities.GameState).where(
            entities.GameState.game_id == game_id
        )
        result = await self._session.execute(stmt)
        return result.scalars().first()

    async def update(self, game_state: entities.GameState) -> None:
        await self._session.execute(
            update(entities.GameState)
            .where(entities.GameState.id == game_state.id)
            .values(
                game_id=game_state.game.id,
                state=game_state.state
            )
        )

    async def create(self, game_state: entities.GameState) -> None:
        self._session.add(game_state)

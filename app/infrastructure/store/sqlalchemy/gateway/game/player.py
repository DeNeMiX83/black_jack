from uuid import UUID
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, delete
from app.infrastructure.store.sqlalchemy.gateway import BaseGateway
from app.core.common.exceptions import GatewayException
from app.core.game.protocols import PlayerGateway
from app.core.game import entities


class PlayerGatewayImpl(BaseGateway, PlayerGateway):
    async def get(self, player_id: UUID, for_update=False) -> entities.Player:
        stmt = select(entities.Player).where(entities.Player.id == player_id)
        if for_update:
            stmt = stmt.with_for_update()
        result = await self._session.execute(stmt)
        return result.scalars().first()

    async def get_players_by_game_id(self, game_id: UUID) -> list[entities.Player]:
        stmt = select(entities.Player).where(
            entities.Player.game_id == game_id
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def create(self, player: entities.Player) -> None:
        self._session.add(player)
        try:
            await self._session.flush()
        except IntegrityError as e:
            await self._session.rollback()
            raise GatewayException(e)

    async def delete_by_id(self, player_id: UUID) -> None:
        stmt = delete(entities.Player).where(entities.Player.id == player_id)
        await self._session.execute(stmt)

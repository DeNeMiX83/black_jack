from sqlalchemy import select
from app.core.user.protocols import UserGateway
from app.infrastructure.store.sqlalchemy.gateway import BaseGateway
from app.core.user import entities


class UserGatewayImpl(BaseGateway, UserGateway):
    async def create(self, user: entities.User) -> None:
        self.session.add(user)

    async def get(self, user_id: int) -> entities.User:
        stmt = select(entities.User).where(entities.User.id == user_id)
        result = await self._session.execute(stmt)
        return result.scalars().first()

    async def get_by_tg_id(self, tg_id: int) -> entities.User:
        stmt = select(entities.User).where(entities.User.tg_id == tg_id)
        result = await self._session.execute(stmt)
        return result.scalars().first()

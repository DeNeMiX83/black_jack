from sqlalchemy import select, update
from app.core.user.protocols import UserGateway
from app.infrastructure.store.sqlalchemy.gateway import BaseGateway
from app.core.user import entities


class UserGatewayImpl(BaseGateway, UserGateway):
    async def create(self, user: entities.User) -> None:
        self._session.add(user)

    async def get(self, user_id: int) -> entities.User:
        stmt = select(entities.User).where(entities.User.id == user_id)
        result = await self._session.execute(stmt)
        return result.scalars().first()

    async def get_by_tg_id(self, tg_id: int) -> entities.User:
        stmt = select(entities.User).where(entities.User.tg_id == tg_id)
        result = await self._session.execute(stmt)
        return result.scalars().first()

    async def get_top_n_users(self, qty: int) -> entities.User:
        stmt = (
            select(entities.User)
            .order_by(entities.User.balance.desc())
            .limit(qty)
        )
        result = await self._session.execute(stmt)
        return result.scalars().fetchall()

    async def update(self, user: entities.User) -> None:
        await self._session.execute(
            update(entities.User)
            .where(entities.User.id == user.id)
            .values(
                tg_id=user.tg_id,
                username=user.username,
                balance=user.balance
            )
        )

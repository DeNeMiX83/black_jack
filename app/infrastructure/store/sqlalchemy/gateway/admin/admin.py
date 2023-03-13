from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from app.infrastructure.store.sqlalchemy.gateway import BaseGateway
from app.core.common.exceptions import GatewayException
from app.core.admin.protocols import AdminGateway
from app.core.admin import entities


class AdminGatewayImpl(BaseGateway, AdminGateway):
    async def get_by_email(self, email: str) -> entities.Admin:
        stmt = select(entities.Admin).where(entities.Admin.email == email)
        result = await self._session.execute(stmt)
        return result.scalars().first()

    async def create(self, admin: entities.Admin) -> entities.Admin:
        self._session.add(admin)
        try:
            await self._session.flush()
        except IntegrityError as e:
            await self._session.rollback()
            raise GatewayException(e)

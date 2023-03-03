from app.core.common.protocols import Commiter
from app.infrastructure.store.sqlalchemy.gateway import BaseGateway


class CommitterImp(BaseGateway, Commiter):
    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()

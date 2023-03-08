from typing import Type, Callable
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.store.sqlalchemy.gateway import BaseGateway


def get_gateway(
    dao_type: Type[BaseGateway],
) -> Callable[[AsyncSession], BaseGateway]:
    def _get_dao(
        session: AsyncSession,
    ) -> BaseGateway:
        return dao_type(session)

    return _get_dao

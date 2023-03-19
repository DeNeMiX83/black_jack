from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.store.sqlalchemy.gateway import (
    UserGatewayImpl,
    CommiterImp,
)
from app.core.user.handlers import GetUserBalanceHandler, GetTopUsersHandler


def get_user_balance_handler_build(
    session: AsyncSession,
) -> GetUserBalanceHandler:
    user_gateway = UserGatewayImpl(session)
    return GetUserBalanceHandler(user_gateway)


def get_top_users_handler_build(
    session: AsyncSession,
) -> GetTopUsersHandler:
    user_gateway = UserGatewayImpl(session)
    return GetTopUsersHandler(user_gateway)

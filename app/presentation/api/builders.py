from sqlalchemy.ext.asyncio import AsyncSession
from app.config.settings import Settings
from app.infrastructure.store.sqlalchemy.gateway import (
    CommiterImp,
    AdminGatewayImpl,
    PlayerGatewayImpl,
)
from app.core.common.services import HasherPasswordServiceImp
from app.core.admin.services import (
    LoginAdminServiceImpl,
)
from app.core.admin.handlers import (
    LoginAdminHandler,
    GetAdminByEmailHandler,
    CreateAdminHandler,
)
from app.core.game.handlers import GetUserStatsOnGamesByTgIdHandler


def login_admin_servise_build(
    session: AsyncSession,
    settings: Settings,
) -> LoginAdminServiceImpl:
    admin_gateway = AdminGatewayImpl(session)
    hasher_password_service = HasherPasswordServiceImp(settings)
    return LoginAdminServiceImpl(admin_gateway, hasher_password_service)


def login_admin_header_build(
    session: AsyncSession, settings: Settings
) -> LoginAdminHandler:
    login_admin_service = login_admin_servise_build(session, settings)
    return LoginAdminHandler(login_admin_service)


def get_admin_by_email_header_build(
    session: AsyncSession,
) -> GetAdminByEmailHandler:
    admin_gateway = AdminGatewayImpl(session)
    return GetAdminByEmailHandler(admin_gateway)


def create_admin_header_build(
    session: AsyncSession, settings: Settings
) -> CreateAdminHandler:
    admin_gateway = AdminGatewayImpl(session)
    hasher_password_service = HasherPasswordServiceImp(settings)
    commiter = CommiterImp(session)
    return CreateAdminHandler(admin_gateway, hasher_password_service, commiter)


def get_user_stats_on_games_by_tg_id_handler_build(
    session: AsyncSession,
) -> GetUserStatsOnGamesByTgIdHandler:
    player_gateway = PlayerGatewayImpl(session)
    return GetUserStatsOnGamesByTgIdHandler(player_gateway)

import asyncio
from aiohttp.web import _run_app
from aiohttp_session import setup as session_setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from aiohttp_apispec import setup_aiohttp_apispec
from app.config.settings import Settings
from app.di.container import Container
from app.infrastructure.store.sqlalchemy.models.mapping import start_mappers
from .middlewares import setup_middlewares
from app.core.admin.exceptions import AdminAlreadyExistsException
from app.core.admin import dto
from app.presentation.api.builders import create_admin_header_build
from app.presentation.api.api.routes import setup_routes
from app.presentation.api.common import Application
from app.presentation.api.api import buildj_di


async def create_admin(email, password, app: Application):
    session = await app.get_session()
    create_admin_header = create_admin_header_build(session, app.settings)
    try:
        await create_admin_header.execute(
            dto.AdminCreate(
                email=email,
                password=password,
            )
        )
    except AdminAlreadyExistsException:
        pass


async def main():
    settings = Settings()
    container = buildj_di.build(Container(), settings)
    app = Application(container, settings)
    setup_aiohttp_apispec(
        app, title="Black jack", url="/docs/json", swagger_path="/docs"
    )
    session_setup(app, EncryptedCookieStorage(settings.session_key))
    setup_middlewares(app)
    setup_routes(app.router)
    start_mappers()
    await create_admin(
        settings.admin_api.admin_email, settings.admin_api.admin_password, app
    )
    await _run_app(
        app, host=settings.admin_api.host, port=settings.admin_api.port
    )


if __name__ == "__main__":
    asyncio.run(main())

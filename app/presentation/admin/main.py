import asyncio
from aiohttp.web import (
    _run_app
)
from aiohttp_session import setup as session_setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from aiohttp_apispec import setup_aiohttp_apispec
from app.settings import Settings
from app.di.container import Container
from .middlewares import setup_middlewares
from app.core.admin.exceptions import AdminAlreadyExistsException
from app.core.admin import dto
from app.presentation.admin.builders import (
    create_admin_header_build
)
from app.presentation.admin.api.routes import setup_routes
from app.presentation.admin.common import Application
from app.presentation.admin.api import buildj_di


async def create_admin(email, password, app: Application):
    session = await app.get_session()
    create_admin_header = create_admin_header_build(
        session,
        app.settings
    )
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
    container = buildj_di.build(Container())
    app = Application(container, settings)
    setup_aiohttp_apispec(
        app, title="Black jack", url="/docs/json", swagger_path="/docs"
    )
    session_setup(app, EncryptedCookieStorage(settings.session_key))
    setup_middlewares(app)
    setup_routes(app.router)
    await create_admin(
        settings.admin_api.admin_email,
        settings.admin_api.admin_password,
        app
    )
    await _run_app(
        app,
        host=settings.admin_api.host,
        port=settings.admin_api.port
    )


if __name__ == "__main__":
    asyncio.run(main())

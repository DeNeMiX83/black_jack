from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from aiohttp.web import (
    Application as AiohttpApplication,
    Request as AiohttpRequest,
    View as AiohttpView,
)
from app.config.settings import Settings
from app.di.container import Container
from app.core.admin import dto as admin_dto


class Application(AiohttpApplication):

    def __init__(self, di: Container, settings: Settings, *args, **kwargs):
        self.settings = settings
        self._di = di
        super().__init__(*args, **kwargs)

    async def get_session(self) -> AsyncSession:
        session = await self._di.resolve(AsyncSession)
        return session


class Request(AiohttpRequest):
    admin: Optional[admin_dto.AdminAuth] = None

    @property
    def app(self) -> Application:
        return super().app()  # type: ignore

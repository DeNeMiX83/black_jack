from typing import Optional
from aiohttp.web import (
    Application as AiohttpApplication,
    Request as AiohttpRequest,
    View as AiohttpView,
)
from app.settings import Settings
from app.core.admin import dto as admin_dto


class Application(AiohttpApplication):
    settings: Settings


class Request(AiohttpRequest):
    admin: Optional[admin_dto.AdminAuth] = None


class View(AiohttpView):
    @property
    def request(self) -> Request:
        return Request(self._request)

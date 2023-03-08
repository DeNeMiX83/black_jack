from typing import Optional
from aiohttp import ClientSession
from app.common.logger import logger
from app.di.container import Container
from app.settings import Settings
from app.infrastructure.tg_api.handler import Handler
from app.infrastructure.tg_api.filters import (
    Filter, MessageFilter, GroupFilter, CommandFilter
)


class TgBot():
    def __init__(self, di: Container):
        self._url: Optional[str] = None
        self._session = ClientSession()
        self._handlers: list[Handler] = []
        self._di = di

    async def start(self):
        from app.infrastructure.tg_api.updates import Updates

        self.settings: Settings = await self._di.resolve(Settings)
        self._url: str = self.settings.tg_api_url_with_token
        updates = await self._di.resolve(Updates)
        await updates.start()

    async def get_handlers(self) -> list[Handler]:
        return self._handlers

    async def send_message(self, **kwargs) -> Optional[dict]:
        url = f"{self._url}/sendMessage"
        async with self._session.get(
            url,
            params={
                **kwargs
            }
        ) as response:
            response.raise_for_status()
            data = await response.json()
            return data

    def message_handler(self, *filters: list[Filter]):
        def decorator(handler_func):
            handler = Handler(handler_func, self._di)
            handler.add_filters([MessageFilter()])
            handler.add_filters(filters)
            self._handlers.append(handler)
            return handler_func
        return decorator

    def common_handler(self, *filters: list[Filter]):
        def decorator(handler_func):
            handler = Handler(handler_func, self._di)
            handler.add_filters(filters)
            self._handlers.append(handler)
            return handler_func
        return decorator

from typing import Optional
from aiohttp import ClientSession
from sqlalchemy.ext.asyncio import AsyncSession
from app.common.logger import logger
from app.di.container import Container
from app.settings import Settings
from app.infrastructure.tg_api.dto import Message
from app.infrastructure.tg_api.handler import Handler
from app.infrastructure.tg_api.filters import (
    Filter, MessageFilter, CallbackQueryFilter
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

    async def get_session(self) -> Container:
        session = await self._di.resolve(AsyncSession)
        return session

    async def get_handlers(self) -> list[Handler]:
        return self._handlers

    async def send_message(self, **kwargs) -> Message:
        url = f"{self._url}/sendMessage"
        async with self._session.get(
            url,
            params={
                **kwargs
            }
        ) as response:
            response.raise_for_status()
            data = await response.json()
            message = Message(**data['result'])
            return message

    async def edit_message_text(self, parse_mode='HTML', **kwargs) -> Message:
        url = f"{self._url}/editMessageText"
        async with self._session.get(
            url,
            params={
                **kwargs,
                'parse_mode': parse_mode
            }
        ) as response:
            response.raise_for_status()
            data = await response.json()
            # message = Message(**data['result'])
            # return message
    
    def message_handler(self, *filters: Filter):
        def decorator(handler_func):
            handler = Handler(handler_func, self._di)
            handler.add_filters([MessageFilter()])
            handler.add_filters(filters)
            self._handlers.append(handler)
            return handler_func
        return decorator

    def callback_query_handler(self, *filters: Filter):
        def decorator(handler_func):
            handler = Handler(handler_func, self._di)
            handler.add_filters([CallbackQueryFilter()])
            handler.add_filters(filters)
            self._handlers.append(handler)
            return handler_func
        return decorator

    def common_handler(self, *filters: Filter):
        def decorator(handler_func):
            handler = Handler(handler_func, self._di)
            handler.add_filters(filters)
            self._handlers.append(handler)
            return handler_func
        return decorator

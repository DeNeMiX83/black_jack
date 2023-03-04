from typing import Optional
from aiohttp import ClientSession
from app.infrastructure.tg_api.handler import Handler
from app.infrastructure.tg_api.filter import Filter


class TgBot():
    def __init__(self, token: str, url: str):
        self._token = token
        self._url = url
        self._session = ClientSession()
        self._handlers: list[Handler] = []

    async def get_handlers(self) -> list[Handler]:
        return self._handlers

    async def send_message(self, chat_id, text) -> Optional[dict]:
        url = f"{self._url}sendMessage"
        async with self._session.get(
            url,
            params={
                chat_id: chat_id,
                text: text
            }
        ) as response:
            response.raise_for_status()
            data = await response.json()
            return data

    def add_handler(self, *filters: list[Filter]):
        def decorator(handler_func):
            handler = Handler(handler_func, self._bot)
            handler.add_filters(filters)
            self._handlers.append(handler)
            return handler_func
        return decorator


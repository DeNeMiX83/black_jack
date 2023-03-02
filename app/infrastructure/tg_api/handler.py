from typing import Protocol
from app.infrastructure.tg_api.dto import Update
from app.infrastructure.tg_api.filter import Filter


class Handler(Protocol):
    def __init__(self, handler_func):
        raise NotImplementedError

    async def handle(self, update: Update) -> None:
        raise NotImplementedError

    async def filter(self, update: Update) -> bool:
        raise NotImplementedError

    def add_filters(self, filters: list[Filter]) -> None:
        raise NotImplementedError


class HandlerBase(Handler):
    def __init__(self, handler_func):
        self._handler_func = handler_func
        self._filters = []

    async def handle(self, update: Update) -> None:
        await self._handler_func(update)

    async def filter(self, update: Update) -> bool:
        for filter in self._filters:
            if not await filter.filter(update):
                return False
        return True

    def add_filters(self, filters: list[Filter]) -> None:
        self._filters.extend(filters)

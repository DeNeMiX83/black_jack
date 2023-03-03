from typing import Protocol, Callable
from app.infrastructure.tg_api.dto import Update
from app.infrastructure.tg_api.filters import Filter


class Handler(Protocol):
    def __init__(self, handler_func: Callable):
        raise NotImplementedError

    async def handle(self, update: Update) -> None:
        raise NotImplementedError

    async def filter(self, update: Update) -> bool:
        raise NotImplementedError

    def add_filters(self, filters: list[Filter]) -> None:
        raise NotImplementedError


class HandlerImpl(Handler):
    def __init__(self, handler_func: Callable):
        self._handler_func = handler_func
        self._filters: list[Filter] = []

    async def handle(self, update: Update) -> None:
        await self._handler_func(update)

    async def filter(self, update: Update) -> bool:
        for handler_filter in self._filters:
            if not await handler_filter.check(update):
                return False
        return True

    def add_filters(self, filters: list[Filter]) -> None:
        self._filters.extend(filters)

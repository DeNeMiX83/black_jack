import inspect
from app.common.logger import logger
from typing import Callable
from sqlalchemy.ext.asyncio import AsyncSession
from app.di.container import Container
from app.infrastructure.tg_api.dto import Update
from app.infrastructure.tg_api.filters import Filter


class Handler():
    def __init__(self, handler_func: Callable, di: Container):
        self._handler_func = handler_func
        self._di = di
        self._filters: list[Filter] = []

    async def handle(self, update: Update) -> None:
        signature = inspect.signature(self._handler_func)
        values = signature.parameters.values()
        dependencies = []
        for value in values:
            if value.name in ('update', 'session'):
                continue
            impl = await self._di.resolve(value.annotation)
            dependencies.append(impl)
        session = await self._di.resolve(AsyncSession)
        await self._handler_func(update, session, *dependencies)

    async def filter(self, update: Update) -> bool:
        for handler_filter in self._filters:
            # print(handler_filter, handler_filter.check(update))
            if not handler_filter.check(update):
                return False
        return True

    def add_filters(self, filters: list[Filter]) -> None:
        self._filters.extend(filters)
import inspect
from typing import Callable, TYPE_CHECKING
from app.di.container import Container
from app.infrastructure.tg_api.dto import Update
from app.infrastructure.tg_api.filters import Filter
from .protocols import Middleware

if TYPE_CHECKING:
    from . import TgBot


class Handler:
    def __init__(
        self,
        handler_func: Callable,
        bot: "TgBot",
        di: Container,
        middleware: list[Middleware],
    ):
        self._handler_func = handler_func
        self._bot = bot
        self._di = di
        self._middlewares = middleware
        self._filters: list[Filter] = []

    async def handle(self, update: Update) -> None:
        dependencies = await self._get_dependencies()
        for middleware in self._middlewares:
            try:
                await middleware(update, self)
            except Exception:
                return

        await self._handler_func(update, *dependencies)

    async def _get_dependencies(self):
        signature = inspect.signature(self._handler_func)
        values = signature.parameters.values()
        dependencies = []
        for value in values:
            if value.name in ("update"):
                continue
            impl = await self._di.resolve(value.annotation)
            dependencies.append(impl)
        return dependencies

    async def filter(self, update: Update) -> bool:
        for handler_filter in self._filters:
            if not handler_filter.check(update):
                return False
        return True

    def add_filters(self, filters: list[Filter]) -> None:
        self._filters.extend(filters)

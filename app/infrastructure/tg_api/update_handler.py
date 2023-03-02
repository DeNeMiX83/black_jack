from app.infrastructure.tg_api.dto import Update
from app.infrastructure.tg_api.handler import Handler
from app.infrastructure.tg_api.filter import Filter


class UpdateHandler:
    def __init__(self):
        self._handlers: list[Handler] = []

    async def handle_updates(self, updates: list[Update]):
        for update in updates:
            await self._handle_update(update)

    async def _handle_update(self, update: Update):
        for handler in self._handlers:
            if await handler.filter(update):
                await handler.handle(update)

    def add_handler(self, filters: list[Filter]):
        def decorator(handler_func):
            handler = Handler(handler_func)
            handler.add_filters(filters)
            self._handlers.append(handler)
            return handler_func
        return decorator

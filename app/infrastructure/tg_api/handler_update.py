from app.infrastructure.tg_api.dto import Update
from app.infrastructure.tg_api.bot import TgBot


class HandlerUpdate:
    def __init__(self, bot: TgBot):
        self._bot = bot

    async def handle_updates(self, updates: list[Update]):
        for update in updates:
            await self._handle_update(update)

    async def _handle_update(self, update: Update):
        for handler in await self._bot.get_handlers():
            if await handler.filter(update):
                await handler.handle(update)

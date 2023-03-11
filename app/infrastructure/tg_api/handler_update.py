from app.common.logger import logger
from app.infrastructure.tg_api.dto import Update
from app.infrastructure.tg_api.bot import TgBot
from app.presentation.tg_bot.states import (
    GameStatesStorage, PlayerStatesStorage
)


class HandlerUpdates:
    def __init__(self, bot: TgBot):
        self._bot = bot

    async def handle_updates(self, updates: list[Update]):
        for update in updates:
            await self._handle_update(update)

    async def _handle_update(self, update: Update):
        game_states_storage = await self._bot._di.resolve(GameStatesStorage)
        player_states_storage = await self._bot._di.resolve(PlayerStatesStorage)

        update.game_states_storage = game_states_storage
        update.player_states_storage = player_states_storage

        for handler in await self._bot.get_handlers():
            if await handler.filter(update):
                await handler.handle(update)

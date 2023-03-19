from app.infrastructure.tg_api.dto import Update
from app.infrastructure.tg_api.bot import TgBot
from app.infrastructure.tg_api.states import (
    GameStateKey,
    PlayerStateKey,
)


class HandlerUpdates:
    def __init__(self, bot: TgBot):
        self._bot = bot

    async def handle_updates(self, updates: list[Update]):
        for update in updates:
            await self.handle_update(update)

    async def handle_update(self, update: Update):
        if update.callback_query is not None:
            chat_id = update.callback_query.message.chat.id
            user_id = update.callback_query.from_user.id
        else:
            chat_id = update.message.chat.id
            user_id = update.message.from_user.id
        game_states_storage = await self._bot.get_game_states_storage()
        player_states_storage = await self._bot.get_player_states_storage()
        game_state_data = await game_states_storage.get_state(
            GameStateKey(chat_id=chat_id)
        )
        player_state_data = await player_states_storage.get_state(
            PlayerStateKey(chat_id=chat_id, user_id=user_id)
        )
        update.game_state_data = game_state_data
        update.player_state_data = player_state_data

        for handler in await self._bot.get_handlers():
            if await handler.filter(update):
                await handler.handle(update)
                break

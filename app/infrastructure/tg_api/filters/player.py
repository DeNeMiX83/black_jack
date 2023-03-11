from app.infrastructure.tg_api.filters import Filter
from app.infrastructure.tg_api.dto import Update
from app.core.game.entities import player_status
from app.presentation.tg_bot.states import PlayerStatesStorage


class PlayerStateFilter(Filter):
    def __init__(self, state: player_status) -> None:
        self._state = state

    def check(
        self,
        update: Update,
    ) -> bool:
        game_states_storage: PlayerStatesStorage = update.player_states_storage
    
        message = update.message
        if update.callback_query is not None:
            message = update.callback_query.message

        chat_id = message.chat.id
        player_data = game_states_storage.get_state(chat_id)
        if player_data and player_data['state'] != self._state:
            return False

        return True

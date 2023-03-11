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
    
        if update.callback_query is not None:
            chat_id = update.callback_query.message.chat.id
            user_id = update.callback_query.from_user.id
        else:
            chat_id = update.message.chat.id
            user_id = update.message.from_user.id
        
        player_data = game_states_storage.get_state((chat_id, user_id))
        if player_data is None:
            return False
        if player_data['state'] != self._state:
            return False

        return True

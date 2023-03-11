from app.infrastructure.tg_api.filters import Filter
from app.infrastructure.tg_api.dto import Update
from app.presentation.tg_bot.states import GameStatesStorage, GameStates


class GameStateFilter(Filter):
    def __init__(self, state: GameStates) -> None:
        self._state = state

    def check(
        self,
        update: Update,
    ) -> bool:
        game_states_storage: GameStatesStorage = update.game_states_storage
    
        message = update.message
        if update.callback_query is not None:
            message = update.callback_query.message

        chat_id = message.chat.id
        game_data = game_states_storage.get_state(chat_id)

        if game_data is None:
            return False
        if game_data['state'] != self._state:
            return False

        return True

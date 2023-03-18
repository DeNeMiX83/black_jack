from app.infrastructure.tg_api.filters import Filter
from app.infrastructure.tg_api.dto import Update
from app.infrastructure.tg_api.states import (
    GameState
)


class GameStateFilter(Filter):
    def __init__(self, state: GameState) -> None:
        self._state = state

    def check(
        self,
        update: Update,
    ) -> bool:

        if update.game_state_data is None:
            return False
        if update.game_state_data.state == GameState.STOP:
            return False
        if update.game_state_data.state != self._state:
            return False

        return True

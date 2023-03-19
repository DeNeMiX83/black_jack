from app.infrastructure.tg_api.filters import Filter
from app.infrastructure.tg_api.dto import Update
from app.infrastructure.tg_api.states import (
    PlayerState,
)


class PlayerStateFilter(Filter):
    def __init__(self, state: PlayerState) -> None:
        self._state = state

    def check(
        self,
        update: Update,
    ) -> bool:
        if update.player_state_data is None:
            return False
        if update.player_state_data.state != self._state:
            return False

        return True

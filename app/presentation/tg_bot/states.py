from typing import Optional
from app.core.game.entities import game_states


class GameStatesStorage():
    def __init__(self):
        self._states: dict[int, dict] = {}

    def add_state(self, chat_id: int, data: dict):
        self._states[chat_id] = data

    def get_state(self, chat_id: int) -> Optional[dict]:
        return self._states.get(chat_id)


class PlayerStatesStorage():
    def __init__(self):
        self._states: dict[tuple[int, int], dict] = {}

    def add_state(self, chat_id: tuple[int, int], data: dict):
        self._states[chat_id] = data

    def get_state(self, chat_id: tuple[int, int]) -> Optional[dict]:
        return self._states.get(chat_id)

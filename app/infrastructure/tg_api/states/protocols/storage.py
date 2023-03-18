from typing import Protocol, Optional


class StatesStorage(Protocol):
    async def add_state(self, chat_id: int, data: dict):
        raise NotImplementedError

    async def get_state(self, chat_id: int) -> Optional[dict]:
        raise NotImplementedError


class GameStatesStorage(StatesStorage):
    ...


class PlayerStatesStorage(StatesStorage):
    ...

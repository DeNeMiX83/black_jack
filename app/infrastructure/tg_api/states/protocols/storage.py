from typing import Protocol, Optional, Any


class StatesStorage(Protocol):
    async def add_state(self, key: Any, data: Any):
        raise NotImplementedError

    async def get_state(self, key: Any) -> Optional[dict]:
        raise NotImplementedError

    async def remove_state(self, key: Any) -> None:
        raise NotImplementedError


class GameStatesStorage(StatesStorage):
    ...


class PlayerStatesStorage(StatesStorage):
    ...

from typing import Optional
from .protocols import GameStatesStorage, PlayerStatesStorage
from .dto import GameStateKey, GameStateData, PlayerStateKey, PlayerStateData
from .protocols import GameStateGateway, PlayerStateGateway


class GameStatesStorageImpl(GameStatesStorage):
    def __init__(self, game_state_gateway: GameStateGateway):
        self._game_state_gateway = game_state_gateway

    async def add_state(self, key: GameStateKey, data: GameStateData):
        await self._game_state_gateway.create(key, data)

    async def get_state(self, key: GameStateKey) -> Optional[dict]:
        result = await self._game_state_gateway.get(key)
        return result

    async def delete_state(self, key: GameStateKey) -> None:
        self._game_state_gateway.delete(key)


class PlayerStatesStorageImpl(PlayerStatesStorage):
    def __init__(self, player_state_gateway: PlayerStateGateway):
        self._player_state_gateway = player_state_gateway

    async def add_state(self, key: PlayerStateKey, data: PlayerStateData):
        await self._player_state_gateway.create(key, data)

    async def get_state(self, key: PlayerStateKey) -> Optional[dict]:
        result = await self._player_state_gateway.get(key)
        return result

    async def delete_state(self, key: PlayerStateKey) -> None:
        self._player_state_gateway.delete(key)

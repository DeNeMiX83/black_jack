from typing import Optional
from uuid import UUID
from ..base import BaseGateway
from app.infrastructure.tg_api.states.protocols import GameStateGateway
from app.infrastructure.tg_api.states.dto import (
    GameStateKey, GameStateData
)
from app.infrastructure.tg_api.states.states import GameState


class GameStateGatewayImp(BaseGateway, GameStateGateway):
    async def create(self, key: GameStateKey, value: GameStateData) -> None:
        composite_key = f'chat_id:{key.chat_id}'
        data_value = value.dict()
        data_value['state'] = data_value['state'].value
        data_value['game_id'] = str(data_value['game_id'])

        await self._redis.hmset(composite_key, data_value)

    async def get(self, key: GameStateKey) -> Optional[GameStateData]:
        composite_key = f'chat_id:{key.chat_id}'
        data = await self._redis.hgetall(composite_key)
        if not data:
            return None
        data = {key.decode(): value.decode() for key, value in data.items()}
        data = GameStateData(
            state=GameState(int(data.get('state'))),
            game_id=UUID(data.get('game_id'))
        )
        return data

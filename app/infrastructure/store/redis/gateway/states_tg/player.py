from typing import Optional
from uuid import UUID
from ..base import BaseGateway
from app.infrastructure.tg_api.states.protocols import PlayerStateGateway
from app.infrastructure.tg_api.states.dto import PlayerStateKey, PlayerStateData
from app.infrastructure.tg_api.states.states import PlayerState


class PlayerStateGatewayImp(BaseGateway, PlayerStateGateway):
    async def create(self, key: PlayerStateKey, value: PlayerStateData) -> None:
        composite_key = f"chat_id:{key.chat_id}:user_id:{key.user_id}"
        data_value = value.dict()
        data_value["state"] = data_value["state"].value
        data_value["player_id"] = str(data_value["player_id"])

        await self._redis.hmset(composite_key, data_value)

    async def get(self, key: PlayerStateKey) -> Optional[PlayerStateData]:
        composite_key = f"chat_id:{key.chat_id}:user_id:{key.user_id}"

        data = await self._redis.hgetall(composite_key)
        if not data:
            return None
        data = {key.decode(): value.decode() for key, value in data.items()}
        data = PlayerStateData(
            state=PlayerState(int(data.get("state"))),
            player_id=UUID(data.get("player_id")),
        )
        return data

    async def delete(self, key: PlayerStateKey) -> None:
        composite_key = f"chat_id:{key.chat_id}:user_id:{key.user_id}"

        await self._redis.delete(composite_key)

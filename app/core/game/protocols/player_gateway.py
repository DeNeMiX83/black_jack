from typing import Protocol
from uuid import UUID
from app.core.game import entities


class PlayerGateway(Protocol):
    async def get(self, player_id: UUID, for_update=False) -> entities.Player:
        raise NotImplementedError

    async def get_players_by_game_id(self, game_id: UUID) -> list[entities.Player]:
        raise NotImplementedError

    async def create(self, player: entities.Player) -> None:
        raise NotImplementedError

    async def delete_by_id(self, player_id: UUID) -> None:
        raise NotImplementedError

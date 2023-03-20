from typing import Protocol
from uuid import UUID
from app.core.user import entities


class UserGateway(Protocol):
    async def get(self, user_id: UUID) -> entities.User:
        raise NotImplementedError

    async def get_by_tg_id(self, tg_id: int) -> entities.User:
        raise NotImplementedError

    async def get_top_n_users(self, qty: int) -> list[entities.User]:
        raise NotImplementedError

    async def update(self, user: entities.User) -> entities.User:
        raise NotImplementedError

    async def create(self, user: entities.User) -> None:
        raise NotImplementedError

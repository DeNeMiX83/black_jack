from typing import Protocol
from app.core.user.entities import User


class UserGateway(Protocol):
    async def get(self, user_id: int) -> User:
        raise NotImplementedError

    async def create(self, user: User) -> User:
        raise NotImplementedError

    async def update(self, user: User) -> User:
        raise NotImplementedError

    async def delete(self, user: User) -> User:
        raise NotImplementedError

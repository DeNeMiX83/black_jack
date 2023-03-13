from typing import Protocol, Optional
from app.core.admin import entities


class AdminGateway(Protocol):
    async def get_by_email(self, email: str) -> Optional[entities.Admin]:
        raise NotImplementedError

    async def create(self, admin: entities.Admin) -> entities.Admin:
        raise NotImplementedError

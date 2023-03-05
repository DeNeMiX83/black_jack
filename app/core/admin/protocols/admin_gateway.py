from typing import Protocol
from app.core.admin import entities


class AdminGateway(Protocol):
    async def get_by_email(self, email: str) -> entities.Admin:
        raise NotImplementedError

from typing import Protocol
from app.core.admin import dto
from app.core.admin import entities


class LoginAdminService(Protocol):
    async def login(self, admin: dto.AdminLogin) -> entities.Admin:
        raise NotImplementedError

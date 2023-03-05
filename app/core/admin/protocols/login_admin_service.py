from typing import Protocol
from app.core.admin import dto


class LoginAdminService(Protocol):
    async def login(self, admin: dto.AdminLogin):
        raise NotImplementedError

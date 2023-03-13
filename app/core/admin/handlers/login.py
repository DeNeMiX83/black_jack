from app.core.common.handler import Handler
from app.core.admin import dto
from app.core.admin.protocols import LoginAdminService
from app.core.admin import entities


class LoginAdminHandler(Handler):
    def __init__(
        self,
        login_admin_service: LoginAdminService,
    ):
        self._login_admin_service = login_admin_service

    async def execute(self, admin: dto.AdminLogin) -> entities.Admin:
        return await self._login_admin_service.login(admin)

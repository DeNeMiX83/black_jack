from app.core.common.handler import Handler
from app.core.admin.exceptions import AdminNotFoundException
from app.core.admin.protocols import AdminGateway
from app.core.admin import entities


class GetAdminByEmailHandler(Handler):
    def __init__(
        self,
        admin_gateway: AdminGateway,
    ):
        self._admin_gateway = admin_gateway

    async def execute(self, email: str) -> entities.Admin:
        admin = await self._admin_gateway.get_by_email(email)

        if not admin:
            raise AdminNotFoundException()
        return admin

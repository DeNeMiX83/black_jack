from app.core.common.protocols import HasherPasswordService
from app.core.admin.exceptions import AuthError
from app.core.admin.protocols import LoginAdminService, AdminGateway
from app.core.admin import dto
from app.core.admin import entities


class LoginAdminServiceImpl(LoginAdminService):
    def __init__(
        self,
        admin_gateway: AdminGateway,
        hashed_password: HasherPasswordService
    ):
        self._hasher_password = hashed_password
        self._admin_gateway = admin_gateway

    async def login(self, admin: dto.AdminLogin) -> entities.Admin:
        admin_entity = await self._admin_gateway.get_by_email(admin.email)

        if not admin_entity:
            raise AuthError("admin not found")
        if not self._hasher_password.verify_password(
            admin.password, admin_entity.password
        ):
            raise AuthError("invalid password")

        return admin_entity

from app.core.common.handler import Handler
from app.core.common.protocols import Commiter, HasherPasswordService
from app.core.common.exceptions import GatewayException
from app.core.admin.exceptions import AdminAlreadyExistsException
from app.core.admin.protocols import AdminGateway
from app.core.admin import dto
from app.core.admin import entities


class CreateAdminHandler(Handler):
    def __init__(
        self,
        admin_gateway: AdminGateway,
        hashed_password: HasherPasswordService,
        commiter: Commiter,
    ):
        self._admin_gateway = admin_gateway
        self._hasher_password = hashed_password
        self._commiter = commiter

    async def execute(self, admin_dto: dto.AdminCreate):
        email = admin_dto.email
        raw_password = admin_dto.password

        hashed_password = self._hasher_password.hash(raw_password)

        admin = entities.Admin(
            email=email,
            password=hashed_password,
        )

        try:
            await self._admin_gateway.create(admin)
        except GatewayException:
            raise AdminAlreadyExistsException

        await self._commiter.commit()

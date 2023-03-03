from app.core.common.handler import Handler
from app.core.common.protocols import Commiter
from app.core.user.protocols import UserGateway
from app.core.user import dto
from app.core.user import entities


class RegisterHandler(Handler):
    def __init__(self, user_gateway: UserGateway, commiter: Commiter):
        self._user_gateway = user_gateway
        self._commiter = commiter

    async def execute(self, user_dto: dto.UserRegister) -> None:
        user = entities.entities.User(
            **user_dto.dict(exclude_unset=True)
        )
        await self._user_gateway.create(user)
        await self._commiter.commit()

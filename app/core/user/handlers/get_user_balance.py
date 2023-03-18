from app.core.common.handler import Handler
from app.core.user.protocols import UserGateway
from app.core.user.exceptions import UserNotFoundException


class GetUserBalanceHandler(Handler):
    def __init__(self, user_gateway: UserGateway):
        self._user_gateway = user_gateway

    async def execute(self, user_tg_id: int) -> int:
        user = await self._user_gateway.get_by_tg_id(user_tg_id)

        if user is None:
            raise UserNotFoundException

        return user.balance

from app.core.common.handler import Handler
from app.core.user.protocols import UserGateway
from app.core.user import entities


class GetTopUsersHandler(Handler):
    def __init__(self, user_gateway: UserGateway):
        self._user_gateway = user_gateway

    async def execute(self, qty: int) -> list[entities.User]:
        users = await self._user_gateway.get_top_n_users(qty)

        return users

from app.core.common.handler import Handler
from app.core.user.protocols import UserGateway
from app.core.common.protocols import Commiter
from app.core.user.exceptions import UserNotFoundException
from app.core.user import dto


class IncreaseUserBalanceHandler(Handler):
    def __init__(self, user_gateway: UserGateway, commiter: Commiter):
        self._user_gateway = user_gateway
        self._commiter = commiter

    async def execute(
        self, increase_user_balance_data: dto.IncreaseUserBalance
    ) -> bool:
        user_tg_id = increase_user_balance_data.user_tg_id
        size_increase = increase_user_balance_data.size_increase

        user = await self._user_gateway.get_by_tg_id(user_tg_id)
        if user.balance > 0:
            return False
        if user is None:
            raise UserNotFoundException

        user.balance += size_increase

        await self._user_gateway.update(user)
        await self._commiter.commit()
        return True

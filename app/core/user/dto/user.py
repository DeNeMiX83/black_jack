from app.common.dto import BaseDto


class UserRegister(BaseDto):
    telegram_id: int
    username: str
    balance: int = 0

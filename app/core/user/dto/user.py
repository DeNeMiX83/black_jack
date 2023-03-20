from pydantic import BaseModel


class UserRegister(BaseModel):
    telegram_id: int
    username: str
    balance: int = 0


class IncreaseUserBalance(BaseModel):
    user_tg_id: int
    size_increase: int

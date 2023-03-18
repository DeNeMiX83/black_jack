from pydantic import BaseModel


class UserRegister(BaseModel):
    telegram_id: int
    username: str
    balance: int = 0

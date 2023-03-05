from app.common.dto import BaseDto


class PlayerCreate(BaseDto):
    tg_id: int
    username: str

from app.common.dto import BaseDto


class ChatCreate(BaseDto):
    tg_id: int
    name: str

from app.common.dto import BaseDto


class Chat(BaseDto):
    tg_id: int
    name: str


class ChatCreate(Chat):
    ...

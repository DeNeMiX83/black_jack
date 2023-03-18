from pydantic import BaseModel


class Chat(BaseModel):
    tg_id: int
    name: str


class ChatCreate(Chat):
    ...

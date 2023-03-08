from typing import Optional
from pydantic import Field
from app.common.dto import BaseDto


class User(BaseDto):
    id: int
    is_bot: bool
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None


class Chat(BaseDto):
    id: int
    type: str
    title: Optional[str]
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]


class MessageEntity(BaseDto):
    type: str
    offset: int
    length: int


class Message(BaseDto):
    message_id: int
    from_user: Optional[User] = Field(alias="from")
    date: int
    chat: Chat
    text: Optional[str] = None
    entities: Optional[list[MessageEntity]] = None
    new_chat_member: Optional[User] = None


class Update(BaseDto):
    update_id: int
    message: Optional[Message] = None
    edited_message: Optional[Message] = None
    channel_post: Optional[Message] = None
    edited_channel_post: Optional[Message] = None
    inline_query: Optional[dict] = None
    chosen_inline_result: Optional[dict] = None
    callback_query: Optional[dict] = None
    shipping_query: Optional[dict] = None
    pre_checkout_query: Optional[dict] = None
    poll: Optional[dict] = None
    poll_answer: Optional[dict] = None
    my_chat_member: Optional[dict] = None
    chat_member: Optional[dict] = None

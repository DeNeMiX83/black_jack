from app.common.dto import BaseDto
from app.core.chat import dto as chat_dto


class GameCreate(BaseDto):
    chat: chat_dto.ChatCreate
    bet: int

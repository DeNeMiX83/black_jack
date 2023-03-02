from app.common.dto import BaseDto
from app.core.chat import dto as chat_dto
from app.core.game import dto as game_dto


class GameCreate(BaseDto):
    chat: chat_dto.ChatCreate
    players: list[game_dto.PlayerCreate]

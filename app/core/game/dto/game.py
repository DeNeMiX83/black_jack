from app.common.dto import BaseDto
from uuid import UUID
from app.core.game import entities as game_entities


class GameCreate(BaseDto):
    chat_tg_id: int


class GameStateUpdate(BaseDto):
    game_id: UUID
    new_state: game_entities.game_states
    current_player: game_entities.Player

from pydantic import BaseModel
from uuid import UUID
from app.core.game import entities as game_entities


class GameCreate(BaseModel):
    chat_tg_id: int


class GameStateUpdate(BaseModel):
    game_id: UUID
    new_state: game_entities.game_states

from pydantic import BaseModel
from uuid import UUID
from .states import GameState as game_states, PlayerState as player_states


class GameStateKey(BaseModel):
    chat_id: int


class GameStateData(BaseModel):
    state: game_states
    game_id: UUID


class PlayerStateKey(BaseModel):
    chat_id: int
    user_id: int


class PlayerStateData(BaseModel):
    state: player_states
    player_id: UUID

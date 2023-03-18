from pydantic import BaseModel
from uuid import UUID
from app.core.game import entities as game_entities


class PlayerCreate(BaseModel):
    tg_id: int
    username: str
    game_id: UUID


class PlayerStateUpdate(BaseModel):
    player_id: UUID
    new_state: game_entities.player_status


class PlayerResult(PlayerStateUpdate):
    winning: int


class PlayerStats(BaseModel):
    state: game_entities.player_status
    score: int
    bet: int


class UserStats(BaseModel):
    games_results: list[PlayerStats]


class Bet(BaseModel):
    player_id: UUID
    bet: int

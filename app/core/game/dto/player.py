from app.common.dto import BaseDto
from uuid import UUID
from app.core.game import entities as game_entities


class PlayerCreate(BaseDto):
    tg_id: int
    username: str
    game_id: UUID


class PlayerStateUpdate(BaseDto):
    player_id: UUID
    new_state: game_entities.player_status


class PlayerResult(PlayerStateUpdate):
    winning: int


class PlayerStats(BaseDto):
    state: game_entities.player_status
    score: int
    bet: int


class UserStats(BaseDto):
    games_results: list[PlayerStats]


class Bet(BaseDto):
    player_id: UUID
    bet: int

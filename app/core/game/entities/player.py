from dataclasses import dataclass, field
from enum import Enum
from app.core.common.entity import Entity
from app.core.user import entities as user_entity
from app.core.game import entities as game_entity


class PlayerStatus(Enum):
    WAIT = 1
    BET = 2
    MOTION = 3
    SKIP = 4
    LOSE = 5
    WIN = 6
    DRAW = 7


@dataclass
class Player(Entity):
    game: game_entity.Game
    user: user_entity.User
    status: PlayerStatus = field(default=PlayerStatus.WAIT)
    score: int = field(default=0)
    bet: int = field(default=0)

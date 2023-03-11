from dataclasses import dataclass, field
from enum import Enum
from app.core.common.entity import Entity
from app.core.user import entities as user_entity
from app.core.game import entities as game_entity


class PlayerStatus(Enum):
    PLAYING = 1
    BET = 2
    WIN = 3
    LOSE = 4


@dataclass
class Player(Entity):
    game: game_entity.Game
    user: user_entity.User
    status: PlayerStatus = field(default=PlayerStatus.PLAYING)
    score: int = field(default=0)
    bet: int = field(default=0)

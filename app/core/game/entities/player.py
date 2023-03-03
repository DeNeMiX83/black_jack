from dataclasses import dataclass, field
from enum import Enum
from app.core.common.entity import Entity
from app.core.user import entities as user_entity
from app.core.game import entities as game_entity


class PlayerStatus(Enum):
    PLAYING = 1
    WIN = 2
    LOSE = 3


@dataclass
class Player(Entity):
    game: game_entity.Game
    user: user_entity.entities.User
    status: PlayerStatus = field(init=False, default=PlayerStatus.PLAYING)
    score: int = field(init=False, default=0)
    bet: int = field(init=False, default=0)

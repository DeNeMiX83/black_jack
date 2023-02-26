from dataclasses import dataclass, field
from app.core.common.entity import Entity
from enum import Enum
from app.core.user import entity


class GameStatus(Enum):
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'


@dataclass
class Game(Entity):
    creator: entity.User
    rate: int = field(default=0)
    status: GameStatus = field(default=GameStatus.IN_PROGRESS)

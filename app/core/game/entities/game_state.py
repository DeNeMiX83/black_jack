from typing import Optional, TYPE_CHECKING
from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING
from app.core.common.entity import Entity
from enum import Enum
from app.core.game import entities as game_entities

if TYPE_CHECKING:
    from app.core.game.entities import Player

if TYPE_CHECKING:
    from app.core.game.entities import Player


class States(Enum):
    START = 'start'
    BET = 'bet'
    MOTION = 'motion'
    STOP = 'stop'


@dataclass
class GameState(Entity):
    game: game_entities.Game
    state: States = field(default=States.START)
    current_player: Optional['Player'] = field(default=None)

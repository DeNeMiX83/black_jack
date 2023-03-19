from typing import Optional
from dataclasses import dataclass, field
from app.core.common.entity import Entity
from enum import Enum
from app.core.game import entities as game_entities


class States(Enum):
    START = "start"
    BET = "bet"
    MOTION = "motion"
    STOP = "stop"


@dataclass
class GameState(Entity):
    game: game_entities.Game
    state: States = field(default=States.START)

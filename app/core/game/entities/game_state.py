from dataclasses import dataclass, field
from typing import Optional
from app.core.common.entity import Entity
from enum import Enum
from app.core.game import entities as game_entities
from app.core.player import players as players_entities


class States(Enum):
    START = 'start'
    BET = 'bet'
    MOTION = 'motion'
    STOP = 'stop'


@dataclass
class GameState(Entity):
    game: game_entities.Game
    state: States = field(default=States.START)
    current_player: Optional[players_entities.Player] = field(default=None)

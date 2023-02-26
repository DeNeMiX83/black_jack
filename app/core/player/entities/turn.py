from dataclasses import dataclass
from app.core.common.entity import Entity
from app.core.player import entities as player_entities
from datetime import datetime


@dataclass
class PlayerCards(Entity):
    player: player_entities.Player
    start_time: datetime

from dataclasses import dataclass, field
from app.core.common.entity import Entity
from app.core.player import entities as player_entities
from app.core.game import entities as game_entities


@dataclass
class PlayerCards(Entity):
    player: player_entities.Player
    cards: list[game_entities.Card] = field(default_factory=list)

from dataclasses import dataclass
from app.core.common.entity import Entity
from app.core.game import entities as game_entities


@dataclass
class PlayerCard(Entity):
    player: game_entities.Player
    card: game_entities.Card

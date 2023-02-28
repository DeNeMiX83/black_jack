from dataclasses import dataclass, field
from app.core.common.entity import Entity
from app.core.chat import entities as chat_entities


@dataclass
class Game(Entity):
    chat: chat_entities.Chat
    bet: int = field(default=0)

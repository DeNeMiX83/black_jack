from dataclasses import dataclass, field
from app.core.common.entity import Entity
from app.core.chat import entities as chat_entities


@dataclass
class Game(Entity):
    chat: chat_entities.Chat
    is_over: bool = field(init=False, default=False)

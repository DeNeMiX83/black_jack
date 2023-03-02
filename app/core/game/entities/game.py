from dataclasses import dataclass
from app.core.common.entity import Entity
from app.core.chat import entities as chat_entities


@dataclass
class Game(Entity):
    chat: chat_entities.Chat

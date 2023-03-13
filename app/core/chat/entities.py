from dataclasses import dataclass
from app.core.common.entity import Entity


@dataclass
class Chat(Entity):
    tg_id: int
    name: str

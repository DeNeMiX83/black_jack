from dataclasses import dataclass, field
from app.core.common.entity import Entity


@dataclass
class User(Entity):
    tg_id: int
    username: str
    balance: int = field(default=0)

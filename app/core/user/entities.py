from dataclasses import dataclass, field
from app.core.common.entity import Entity


@dataclass
class User(Entity):
    name: str
    balance: int = field(default=0)

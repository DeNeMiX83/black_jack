from typing import Optional
from dataclasses import dataclass, field
from app.core.common.entity import Entity


@dataclass
class Admin(Entity):
    id: Optional[int] = field(init=False, default=None)
    email: str
    password: str

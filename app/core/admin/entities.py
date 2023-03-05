from dataclasses import dataclass
from app.core.common.entity import Entity


@dataclass
class Admin(Entity):
    email: str
    password: str

from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID


@dataclass
class Entity:
    id: Optional[UUID] = field(default=None)

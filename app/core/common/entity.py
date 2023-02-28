from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Entity():
    id: Optional[str] = field(init=False, default=None)

from dataclasses import dataclass, field
from app.core.common.entity import Entity


@dataclass
class Card(Entity):
    rank: str
    weight: int = field(init=False)

    def __post_init__(self):
        self.weight = self._get_weight()

    def _get_weight(self) -> int:
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 11
        else:
            return int(self.rank)

    def __composite_values__(self):
        return (
            self.rank,
            self.weight,
        )

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Enum, ForeignKey
from sqlalchemy.orm import relationship
import uuid

from app.infrastructure.store.sqlalchemy.models import Base

from app.core.game import entities


class GameState(Base):
    __tablename__ = "game_state"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    game_id = Column(
        "game_id",
        UUID(as_uuid=True),
        ForeignKey("game.id", ondelete="CASCADE"),
        nullable=False,
    )
    state = Column(Enum(entities.game_states), nullable=False)


def game_state_mapping(mapper_registry):
    table = GameState.__table__
    mapper_registry.map_imperatively(
        entities.GameState,
        table,
        properties={
            "game": relationship(entities.Game, lazy="joined"),
        },
    )

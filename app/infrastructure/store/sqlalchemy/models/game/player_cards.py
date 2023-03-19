from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, composite

import uuid

from app.infrastructure.store.sqlalchemy.models import Base

from app.core.game import entities as game_entities


class PlayerCards(Base):
    __tablename__ = "player_cards"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    player_id = Column(UUID(as_uuid=True), ForeignKey("player.id"))
    rank = Column(String, nullable=False)
    weight = Column(Integer, nullable=False)


def player_cards_mapping(mapper_registry):
    table = PlayerCards.__table__
    mapper_registry.map_imperatively(
        game_entities.PlayerCard,
        table,
        properties={
            "player": relationship(game_entities.Player, lazy="joined"),
            "card": composite(game_entities.Card, table.c.rank, table.c.weight),
        },
    )

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Enum, ForeignKey
from sqlalchemy.orm import relationship
import uuid

from app.infrastructure.store.sqlalchemy.model import Base

from app.core.game import entities


class GameState(Base):
    __tablename__ = 'game_state'

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    _game_id = Column(
        'game_id',
        UUID(as_uuid=True), ForeignKey('game.id'), nullable=False
    )
    state = Column(Enum(entities.game_states), nullable=False)
    _current_player_id = Column(
        'current_player_id',
        UUID(as_uuid=True), ForeignKey('player.id'), nullable=False
    )

    game = relationship('Game')
    current_player = relationship('Player')


def game_state_mapping(mapper_registry):
    table = GameState.__table__
    mapper_registry.map_imperatively(
        entities.GameState,
        table,
        properties={
            'game': relationship(entities.Game),
            'current_player': relationship(entities.Player),
        }
    )

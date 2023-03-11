from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Enum, Integer, ForeignKey, Index
from sqlalchemy.orm import relationship
import uuid

from app.infrastructure.store.sqlalchemy.models import Base

from app.core.game import entities as game_entities
from app.core.user import entities as user_entities


class Player(Base):
    __tablename__ = 'player'

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    game_id = Column('game_id', UUID(as_uuid=True), ForeignKey('game.id', ondelete='CASCADE'))
    user_id = Column('user_id', UUID(as_uuid=True), ForeignKey('user.id'))
    status = Column(Enum(game_entities.player_status), nullable=False)
    score = Column(Integer, nullable=False)
    bet = Column(Integer, nullable=False)

    __table_args__ = (
        Index('idx_game_id_user_id', game_id, user_id, unique=True),
    )


def player_mapping(mapper_registry):
    table = Player.__table__
    mapper_registry.map_imperatively(
        game_entities.Player,
        table,
        properties={
            'game': relationship(game_entities.Game, lazy='joined'),
            'user': relationship(user_entities.User, lazy='joined')
        }
    )

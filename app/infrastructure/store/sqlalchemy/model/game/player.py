from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Enum, Integer, ForeignKey
from sqlalchemy.orm import relationship
import uuid

from app.infrastructure.store.sqlalchemy.model import Base

from app.core.player import entities


class Player(Base):
    __tablename__ = 'player'

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    _game_id = Column('game_id', UUID(as_uuid=True), ForeignKey('game.id'))
    _user_id = Column('user_id', UUID(as_uuid=True), ForeignKey('user.id'))
    status = Column(Enum(entities.player_status), nullable=False)
    score = Column(Integer, nullable=False)
    bet = Column(Integer, nullable=False)

    game = relationship('Game')
    user = relationship('User')


def player_mapping(mapper_registry):
    table = Player.__table__
    mapper_registry.map_imperatively(
        entities.Player,
        table,
        properties={
            'game': relationship(entities.Game),
            'user': relationship(entities.User)
        }
    )

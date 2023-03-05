from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
import uuid

from app.infrastructure.store.sqlalchemy.model import Base

from app.core.chat import entities as chat_entities
from app.core.game import entities as game_entities


class Game(Base):
    __tablename__ = 'game'

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    _chat_id = Column('chat_id', UUID(as_uuid=True), ForeignKey('chat.id'))

    chat = relationship('Chat')


def game_mapping(mapper_registry):
    table = Game.__table__
    mapper_registry.map_imperatively(
        game_entities.Game,
        table,
        properties={
            'chat': relationship(chat_entities.Chat)
        }
    )

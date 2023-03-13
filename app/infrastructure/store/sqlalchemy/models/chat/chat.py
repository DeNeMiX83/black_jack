from sqlalchemy import Column, String, BigInteger
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.infrastructure.store.sqlalchemy.models import Base

from app.core.chat import entities


class Chat(Base):
    __tablename__ = 'chat'

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    tg_id = Column(BigInteger, nullable=False, unique=True)
    name = Column(String, nullable=False)


def chat_mapping(mapper_registry):
    table = Chat.__table__
    mapper_registry.map_imperatively(
        entities.Chat,
        table
    )

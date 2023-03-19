from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, BigInteger, Integer
import uuid

from app.infrastructure.store.sqlalchemy.models import Base

from app.core.user import entities


class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tg_id = Column(BigInteger, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    balance = Column(Integer, nullable=False, default=0)


def user_mapping(mapper_registry):
    table = User.__table__
    mapper_registry.map_imperatively(
        entities.User,
        table,
    )

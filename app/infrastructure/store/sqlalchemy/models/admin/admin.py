from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer
import uuid

from app.infrastructure.store.sqlalchemy.models import Base

from app.core.admin import entities


class Admin(Base):
    __tablename__ = "admin"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)


def admin_mapping(mapper_registry):
    table = Admin.__table__
    mapper_registry.map_imperatively(
        entities.Admin,
        table,
    )

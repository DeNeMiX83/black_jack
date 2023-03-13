from app.di.container import Container
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.store.sqlalchemy.factories import (
    create_session_factory
)


def build(container: Container) -> Container:
    container.register(AsyncSession, create_session_factory)

    return container

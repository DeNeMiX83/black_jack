from sqlalchemy.ext.asyncio import AsyncSession
from app.settings import Settings
from app.di.container import Container
from app.infrastructure.store.sqlalchemy.factories import (
    create_session_factory
)


def build(container: Container, settings: Settings) -> Container:
    container.register(Settings, settings)
    container.register(AsyncSession, create_session_factory)

    return container

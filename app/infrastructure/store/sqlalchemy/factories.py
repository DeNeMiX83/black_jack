from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from app.config.settings import Settings


async def create_session_factory(settings: Settings):
    engine = create_async_engine(settings.postgres.url, echo=False)

    async_session = async_sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    async with async_session() as session:
        yield session

    await engine.dispose()

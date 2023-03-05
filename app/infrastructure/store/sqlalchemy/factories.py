from typing import Callable
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)


def create_session_factory(url: str) -> Callable[[], AsyncSession]:
    engine = create_async_engine(url, echo=True)

    async_session = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async def session_factory():
        async with async_session() as session:
            yield session

    return session_factory

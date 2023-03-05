from typing import Protocol
from sqlalchemy.ext.asyncio import AsyncSession


class Gateway(Protocol):
    def __init__(self, session: AsyncSession) -> None:
        raise NotImplementedError


class BaseGateway(Gateway):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

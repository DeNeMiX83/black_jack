from typing import Protocol
from app.infrastructure.tg_api.dto import Update


class Filter(Protocol):
    async def check(self, update: Update) -> bool:
        raise NotImplementedError

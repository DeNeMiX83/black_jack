from typing import Protocol, TYPE_CHECKING
from .dto import Update

if TYPE_CHECKING:
    from . import Handler


class Middleware(Protocol):
    async def __call__(self, update: Update, handler: "Handler"):
        raise NotImplementedError

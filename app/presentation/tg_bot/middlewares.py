from typing import Callable
import time
import logging
from app.infrastructure.tg_api.dto import Update
from app.infrastructure.tg_api import TgBot, Handler
from app.infrastructure.tg_api.protocols import Middleware

logger = logging.getLogger()


def throttling_rate(rate_limit):
    def wrapper(handler: Handler):
        setattr(handler, "rate_limit", rate_limit)

    return wrapper


class ThrottlingMiddleware(Middleware):
    def __init__(self, bot: TgBot):
        self._storage: dict = {}
        self._bot = bot

    async def __call__(self, update: Update, handler: Handler):
        if update.callback_query is not None:
            chat_id = update.callback_query.message.chat.id  # type: ignore
            user = update.callback_query.from_user
        else:
            chat_id = update.message.chat.id  # type: ignore
            user = update.message.from_user  # type: ignore
        user_id = user.id  # type: ignore
        user_name = user.username  # type: ignore

        key = (handler._handler_func.__name__, chat_id, user_id)
        if key not in self._storage:
            self._storage[key] = {
                "last_update_time": time.time(),
                "count": 1,
                "notify": True,
            }
        else:
            rate_limit = getattr(handler, "rate_limit", 0)
            if rate_limit == 0:
                return
            if (
                time.time() - self._storage[key]["last_update_time"]
                < rate_limit
            ):
                logger.warning(f"User {user_id} is throttled")
                if self._storage[key]["notify"]:
                    await self._bot.send_message(
                        chat_id=chat_id,
                        text=f"@{user_name} блокировка на {rate_limit} сек.",
                    )
                self._storage[key]["notify"] = False
                raise Exception(f"User {user_id} is throttled")

        self._storage[key]["last_update_time"] = time.time()
        self._storage[key]["count"] += 1
        self._storage[key]["notify"] = True

from typing import Optional, Callable, TYPE_CHECKING
from aiohttp import ClientSession
from sqlalchemy.ext.asyncio import AsyncSession
from app.di.container import Container
from app.config.settings import Settings
from .states.protocols import GameStatesStorage, PlayerStatesStorage
from .protocols import Middleware
from app.infrastructure.tg_api.dto import Update, Message
from app.infrastructure.tg_api.handler import Handler
from app.infrastructure.tg_api.filters import (
    Filter,
    MessageFilter,
    CallbackQueryFilter,
)

if TYPE_CHECKING:
    from app.infrastructure.tg_api.handler_update import HandlerUpdates


class TgBot:
    def __init__(self, settings: Settings, di: Container):
        self._url: Optional[str] = None
        self._session = ClientSession()
        self._handlers: list[Handler] = []
        self._handler_updates: "HandlerUpdates"
        self._game_states_storage: GameStatesStorage
        self._player_states_storage: PlayerStatesStorage
        self._middlewares: list[Middleware] = []
        self.settings = settings
        self._di = di

    async def start(self):
        from app.infrastructure.tg_api.handler_update import (
            Updates,
            HandlerUpdates,
        )

        self._game_states_storage = await self._di.resolve(GameStatesStorage)
        self._player_states_storage = await self._di.resolve(
            PlayerStatesStorage
        )

        self._handler_updates = await self._di.resolve(HandlerUpdates)
        self._url: str = self.settings.tg_api_url_with_token

        updates = await self._di.resolve(Updates)
        await updates.start()

    async def get_session(self) -> AsyncSession:
        session = await self._di.resolve(AsyncSession)
        return session

    async def get_handlers(self) -> list[Handler]:
        return self._handlers

    async def get_game_states_storage(self) -> GameStatesStorage:
        return self._game_states_storage

    async def get_player_states_storage(self) -> PlayerStatesStorage:
        return self._player_states_storage

    async def seng_update(self, update: Update) -> None:
        await self._handler_updates.handle_updates([update])

    def add_middleware(self, middleware: Middleware):
        self._middlewares.append(middleware)

    async def send_message(self, **kwargs) -> Message:
        url = f"{self._url}/sendMessage"
        async with self._session.get(url, params={**kwargs}) as response:
            response.raise_for_status()
            data = await response.json()
            message = Message(**data["result"])
            return message

    async def edit_message_text(self, parse_mode="HTML", **kwargs) -> Message:
        url = f"{self._url}/editMessageText"
        async with self._session.get(
            url, params={**kwargs, "parse_mode": parse_mode}
        ) as response:
            response.raise_for_status()

    async def delete_message(self, **kwargs):
        url = f"{self._url}/deleteMessage"
        async with self._session.get(url, params={**kwargs}) as response:
            response.raise_for_status()

    def message_handler(self, *filters: Filter):
        def decorator(handler_func):
            new_filters = (MessageFilter(),) + filters
            return self._create_handler(handler_func, new_filters)

        return decorator

    def callback_query_handler(self, *filters: Filter):
        def decorator(handler_func):
            new_filters = (CallbackQueryFilter(),) + filters
            return self._create_handler(handler_func, new_filters)

        return decorator

    def common_handler(self, *filters: Filter):
        def decorator(handler_func):
            return self._create_handler(handler_func, filters)

        return decorator

    def _create_handler(
        self, handler_func: Callable, filters: list[Filter]
    ) -> Handler:
        handler = Handler(
            handler_func=handler_func,
            bot=self,
            di=self._di,
            middleware=self._middlewares,
        )
        handler.add_filters(filters)
        self._handlers.append(handler)
        return handler

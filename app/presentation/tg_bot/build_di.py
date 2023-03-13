
from app.di import Container
from app.settings import Settings
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.store.sqlalchemy.factories import (
    create_session_factory
)

from app.infrastructure.tg_api import HandlerUpdates, Poller, Updates
from app.presentation.tg_bot.builds import chat_build, game_build


def build(container: Container) -> None:
    settings = Settings()

    container.register(Settings, settings)
    container.register(AsyncSession, create_session_factory)
    container.register(HandlerUpdates, HandlerUpdates)
    container.register(Poller, build_poller(settings))
    container.register(Updates, Updates)
    chat_build(container)
    game_build(container)


def build_poller(settings: Settings) -> Poller:
    return Poller(settings.tg_api_url_with_token)

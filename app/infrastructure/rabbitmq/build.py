from app.settings import Settings
from .tg_updates import TgUpdates


def build_rabbit_tg_updates(
    settings: Settings,
) -> TgUpdates:
    return TgUpdates(
        settings.rabbitmq.url,
        settings.rabbitmq.queue,
    )

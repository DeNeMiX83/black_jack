import asyncio
from app.settings import Settings
from .tg_poller import TgPoller
from .publisher import RabbitMQUpdatePublisher
from .tg_updates import TgUpdates


async def main():
    settings = Settings()

    tg_poller = TgPoller(
        settings.tg_api_url_with_token
    )

    publicher = RabbitMQUpdatePublisher(
        settings.rabbitmq.url,
        settings.rabbitmq.queue
    )

    tg_updates = TgUpdates(
        tg_poller,
        publicher
    )

    await tg_updates.start()


if __name__ == '__main__':
    asyncio.run(main())

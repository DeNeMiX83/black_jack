import asyncio
from app.infrastructure.rabbitmq.publisher import RabbitMQUpdatePublisher
from app.infrastructure.rabbitmq.tg_poller import TgPoller


class TgUpdates:
    def __init__(
        self,
        poller: TgPoller,
        publisher: RabbitMQUpdatePublisher,
    ):
        self._poller = poller
        self._publisher = publisher
        self._is_running = False

    async def start(self):
        await self._poller.connect()
        await self._publisher.connect()
        self._is_running = True
        await self.poll()

    async def poll(self):
        while self._is_running:
            try:
                updates = await self._poller.get_updates()
                for update in updates:
                    await self.process_update(update)
            except Exception:
                await asyncio.sleep(5)

    async def process_update(self, update: dict):
        try:
            await self._publisher.publish_update(update)
        except Exception:
            ...

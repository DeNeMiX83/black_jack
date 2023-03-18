import json
import aio_pika
from app.infrastructure.tg_api.dto import Update


class RabbitMQPoller:
    def __init__(
        self,
        rabbitmq_url: str,
        rabbitmq_queue: str,
    ):
        self._rabbitmq_url = rabbitmq_url
        self._rabbitmq_queue = rabbitmq_queue
        self._is_polling = False

    async def connect(self):
        connection = await aio_pika.connect_robust(self._rabbitmq_url)
        channel = await connection.channel()
        self._queue = await channel.declare_queue(
            self._rabbitmq_queue, durable=True
        )

    async def stop(self):
        self._is_polling = False

    async def get_update(self):
        async with self._queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    return Update(**json.loads(message.body))

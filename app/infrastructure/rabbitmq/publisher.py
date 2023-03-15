import json
import aio_pika


class RabbitMQUpdatePublisher:
    def __init__(
        self,
        rabbitmq_url: str,
        rabbitmq_queue: str,
    ):
        self._rabbitmq_url = rabbitmq_url
        self._rabbitmq_queue = rabbitmq_queue

    async def connect(self):
        connection = await aio_pika.connect_robust(self._rabbitmq_url)
        self._channel = await connection.channel()
        await self._channel.declare_queue(
            self._rabbitmq_queue, durable=True
        )

    async def publish_update(self, update: dict):
        await self._channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps(update).encode()),
            routing_key=self._rabbitmq_queue,
        )

    async def close(self):
        await self._connection.close()

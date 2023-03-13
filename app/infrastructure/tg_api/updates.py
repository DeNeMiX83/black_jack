import asyncio
from asyncio import Task
from typing import Optional
from app.infrastructure.tg_api.rabbit_poller import RabbitMQPoller
from app.infrastructure.tg_api.handler_update import HandlerUpdates


class Updates:
    def __init__(self, poller: RabbitMQPoller, handler_updates: HandlerUpdates):
        self._poller = poller
        self._handler_updates = handler_updates
        self._is_running = False
        self._poll_task: Optional[Task] = None

    async def start(self):
        await self._poller.connect()
        self._is_running = True
        await self.poll()

    async def poll(self):
        while self._is_running:
            try:
                update = await self._poller.get_update()
                task = asyncio.create_task(
                    self._handler_updates.handle_update(update)
                )
                task.add_done_callback(lambda fn: print(fn))
            except Exception:
                await asyncio.sleep(5)

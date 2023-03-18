import sys
import traceback
import asyncio
from asyncio import Task
from typing import Optional
from app.infrastructure.tg_api.handler_update import (
    RabbitMQPoller, HandlerUpdates
)


class Updates:
    def __init__(
        self,
        poller: RabbitMQPoller,
        handler_updates: HandlerUpdates
    ):
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
                asyncio.create_task(
                    self._handler_updates.handle_update(update)
                )
            except Exception:
                exc_info = sys.exc_info()
                print("Traceback:")
                traceback.print_exception(*exc_info)
                await asyncio.sleep(5)

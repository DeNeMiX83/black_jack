import sys
import traceback
import asyncio
import logging
from asyncio import Task
from typing import Optional
from app.infrastructure.tg_api.handler_update import (
    RabbitMQPoller,
    HandlerUpdates,
)

logger = logging.getLogger()


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
                task.add_done_callback(self.handle_future)
            except Exception:
                exc_info = sys.exc_info()
                print("Traceback:")
                traceback.print_exception(*exc_info)
                await asyncio.sleep(5)

    def handle_future(future: asyncio.Future):
        if future.exception():
            logger.exception(future.exception())

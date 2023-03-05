import asyncio
from asyncio import Task
from typing import Optional
from app.infrastructure.tg_api import Poller, Handler


class Updates:
    def __init__(self, poller: Poller, handler: Handler):
        self._poller = poller
        self._handler = handler
        self._is_running = False
        self._poll_task: Optional[Task] = None

    async def start(self):
        self._is_running = True
        await self.poll()

    async def poll(self):
        while self._is_running:
            try:
                updates = await self._poller.get_updates()
                asyncio.create_task(self._handler.handle_updates(updates))
            except Exception:
                await asyncio.sleep(5)

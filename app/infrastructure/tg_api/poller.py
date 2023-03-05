from typing import Optional
from aiohttp import TCPConnector
from aiohttp.client import ClientSession


class Poller:
    def __init__(self, server_url: str):
        self.session: Optional[ClientSession] = None
        self.server_url: str = server_url
        self._offset = 0

    async def connect(self):
        self.session = ClientSession(connector=TCPConnector(verify_ssl=False))

    async def disconnect(self):
        if self.session:
            await self.session.close()

    async def get_updates(self):
        async with self.session.get(
            self.server_url + 'getUpdates',
            data={
                'timeout': 30,
                'offset': self._offset,
            }
        ) as resp:
            resp.raise_for_status()
            data = await resp.json()
            updates = data['result']
            self._offset = updates[-1]['update_id'] + 1
            return updates

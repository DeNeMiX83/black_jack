from typing import Optional
from aiohttp import TCPConnector
from aiohttp.client import ClientSession


class TgPoller():
    def __init__(
        self,
        server_url: str,
    ):
        self.server_url: str = server_url
        self._session: Optional[ClientSession] = None
        self._offset = 0

    async def connect(self):
        self._session = ClientSession()

    async def get_updates(self):
        async with self._session.get(
            self.server_url + '/getUpdates',
            params={
                'timeout': 30,
                'offset': self._offset,
            }
        ) as resp:
            resp.raise_for_status()

            data = await resp.json()
            data = data['result']
            self._offset = data[-1]['update_id'] + 1
            return data

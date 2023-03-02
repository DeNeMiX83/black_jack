from typing import Optional
from aiohttp import ClientSession


class TgBot():
    def __init__(self, token, url):
        self._token = token
        self._url = url
        self._session = ClientSession()

    async def send_message(self, chat_id, text) -> Optional[dict]:
        url = f"{self._url}sendMessage?chat_id={chat_id}&text={text}"
        async with self._session.get(url) as response:
            response.raise_for_status()
            data = await response.json()
            return data

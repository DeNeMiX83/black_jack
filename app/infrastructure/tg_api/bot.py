from typing import Optional
from aiohttp import ClientSession


class TgBot():
    def __init__(self, token: str, url: str):
        self._token = token
        self._url = url
        self._session = ClientSession()

    async def send_message(self, chat_id, text) -> Optional[dict]:
        url = f"{self._url}sendMessage"
        async with self._session.get(
            url,
            params={
                chat_id: chat_id,
                text: text
            }
        ) as response:
            response.raise_for_status()
            data = await response.json()
            return data

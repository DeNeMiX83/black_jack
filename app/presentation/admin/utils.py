from typing import Any, Optional

from aiohttp.web import json_response as aiohttp_json_response
from aiohttp.web_response import Response
from aiohttp_session import get_session


def json_response(data: Any = None, status: str = "ok") -> Response:
    if data is None:
        data = {}
    return aiohttp_json_response(
        data={
            "status": status,
            "data": data,
        }
    )


def error_json_response(
    http_status: int,
    status: str = "error",
    message: Optional[str] = None,
    data: Optional[dict] = None,
):
    if data is None:
        data = {}
    return aiohttp_json_response(
        status=http_status,
        data={
            "status": status,
            "message": str(message),
            "data": data,
        },
    )


def auth_required(func):
    async def wrapper(self, *args, **kwargs):
        session = await get_session(self.request)

        print(session, 34242134123412341234)
        if session.get("admin") is None:
            return error_json_response(
                http_status=401,
                status="unauthorized",
            )

        self.session = session
        return await func(self, *args, **kwargs)

    return wrapper
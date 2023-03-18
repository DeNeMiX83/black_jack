import json
from uuid import UUID
from typing import Callable
from aiohttp.web_exceptions import HTTPException, HTTPUnprocessableEntity
from aiohttp.web_middlewares import middleware
from aiohttp_apispec import validation_middleware
from aiohttp_session import (
    Session, session_middleware, cookie_storage, get_session
)
from app.presentation.api.responses import error_json_response
from app.presentation.api.common import Application, Request
from app.core.admin import dto as admin_dto


@middleware
async def auth_middleware(request: Request, handler: Callable):
    session = await get_session(request)
    if session:
        request.admin = get_admin_from_session(session)
    return await handler(request)


def get_admin_from_session(
    session: Session
) -> admin_dto.AdminAuth:
    return admin_dto.AdminAuth(
        id=session["admin"]["id"],
        email=session["admin"]["email"]
    )


HTTP_ERROR_CODES = {
    400: "bad_request",
    401: "unauthorized",
    403: "forbidden",
    404: "not_found",
    405: "not_implemented",
    409: "conflict",
    500: "internal_server_error",
}


@middleware
async def error_handling_middleware(request: Request, handler: Callable):
    try:
        response = await handler(request)
        return response
    except HTTPUnprocessableEntity as e:
        return error_json_response(
            http_status=400,
            status="bad_request",
            message=e.reason,
            data=json.loads(e.text),  # type: ignore
        )
    except HTTPException as e:
        return error_json_response(
            http_status=e.status,
            status=HTTP_ERROR_CODES[e.status],
            message=str(e),
        )
    except Exception as e:
        request.app.logger.error("Exception", exc_info=e)
        return error_json_response(
            http_status=500, status="internal server error"
        )


def setup_middlewares(app: Application):
    app.middlewares.append(error_handling_middleware)  # type: ignore
    app.middlewares.append(validation_middleware)
    app.middlewares.append(auth_middleware)  # type: ignore
    app.middlewares.append(
        session_middleware(
            cookie_storage.EncryptedCookieStorage(
                app.settings.session_key,
            ),
        ),
    )


from aiohttp.web import (
    Response,
    RouteTableDef,
    HTTPForbidden
)
from aiohttp_apispec import request_schema, response_schema, docs
from aiohttp_session import new_session, get_session
from app.presentation.api.common import Request
from .schemes import AdminRequestSchema, AdminResponseSchema
from app.core.admin.exceptions import (
    AuthError,
    AdminNotFoundException
)
from app.core.admin import dto
from app.presentation.api.responses import json_response
from app.presentation.api.builders import (
    login_admin_header_build,
    get_admin_by_email_header_build
)

router = RouteTableDef()


@docs(tags=['admin'])  # type: ignore
@request_schema(AdminRequestSchema())  # type: ignore
@response_schema(AdminResponseSchema())
@router.post("/admin.login")
async def admin_login(request: Request) -> Response:
    session = await request.app.get_session()
    settings = request.app.settings
    login_admin_header = login_admin_header_build(session, settings)

    data = request.get("data")
    try:
        admin = await login_admin_header.execute(
            dto.AdminLogin(
                email=data["email"],  # type: ignore
                password=data["password"]  # type: ignore
            )
        )
        ai_session = await new_session(request)
        ai_session["admin"] = {"email": admin.email, "id": admin.id}
    except AuthError:
        raise HTTPForbidden

    return json_response(AdminResponseSchema().dump(admin))


@docs(tags=['admin'])  # type: ignore
@response_schema(AdminResponseSchema())  # type: ignore
@router.get("/admin.current", allow_head=False)
async def get_current_admin(request: Request) -> Response:
    session = await request.app.get_session()
    get_admin_by_email_header = get_admin_by_email_header_build(session)

    ai_session = await get_session(request)
    email = ai_session.get("admin", {}).get("email")
    if email:
        try:
            admin = await get_admin_by_email_header.execute(email)
            return json_response(AdminResponseSchema().dump(admin))
        except AdminNotFoundException:
            raise HTTPForbidden
    raise HTTPForbidden

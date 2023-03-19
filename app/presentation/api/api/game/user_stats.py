from aiohttp.web import Response, RouteTableDef, HTTPForbidden
from aiohttp_apispec import response_schema, docs
from app.presentation.api.common import Request
from .schemes import UserStatsResponseSchema
from app.core.game.exceptions import PlayerNotFoundException
from app.presentation.api.responses import json_response
from app.presentation.api.builders import (
    get_user_stats_on_games_by_tg_id_handler_build,
)

router = RouteTableDef()


@docs(tags=["user"])  # type: ignore
@response_schema(UserStatsResponseSchema())
@router.get("/user/{tg_id}", allow_head=False)
async def user_stats(request: Request) -> Response:
    tg_id = request.match_info.get("tg_id", None)

    if not tg_id:
        raise HTTPForbidden

    session = await request.app.get_session()
    handler = get_user_stats_on_games_by_tg_id_handler_build(session)
    try:
        user_stats = await handler.execute(int(tg_id))
    except PlayerNotFoundException:
        raise HTTPForbidden

    return json_response(UserStatsResponseSchema().dump(user_stats))

from aiohttp.web import UrlDispatcher
from .admin import admin_router
from .game import user_stats_router


def setup_routes(router: UrlDispatcher) -> None:
    router.add_routes(admin_router)
    router.add_routes(user_stats_router)

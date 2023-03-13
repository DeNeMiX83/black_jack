from aiohttp.web import UrlDispatcher
from .admin import admin_router


def setup_routes(router: UrlDispatcher) -> None:
    router.add_routes(admin_router)

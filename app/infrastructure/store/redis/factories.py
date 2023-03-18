from redis.asyncio import Redis
from app.config.settings import Settings


def redis_factory(settings: Settings) -> Redis:
    return Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        db=settings.redis.db,
    )

from typing import Protocol
from redis.asyncio import Redis


class Gateway(Protocol):
    def __init__(self, redis) -> None:
        raise NotImplementedError


class BaseGateway(Gateway):
    def __init__(self, redis: Redis) -> None:
        self._redis = redis

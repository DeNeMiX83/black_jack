
from app.di import Container
from app.config.settings import Settings
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from app.infrastructure.store.sqlalchemy.factories import (
    create_session_factory
)
from app.infrastructure.store.redis.factories import redis_factory

from app.infrastructure.tg_api.handler_update import (
    HandlerUpdates, RabbitMQPoller, Updates
)
from app.infrastructure.store.redis.gateway import (
    GameStateGatewayImp, PlayerStateGatewayImp
)
from app.infrastructure.tg_api.states.protocols import (
    GameStateGateway, PlayerStateGateway,
    GameStatesStorage, PlayerStatesStorage
)
from app.infrastructure.tg_api.states import (
    GameStatesStorageImpl, PlayerStatesStorageImpl
)


def build(container: Container) -> None:
    settings = Settings()

    container.register(AsyncSession, create_session_factory)
    container.register(Redis, redis_factory)
    container.register(GameStateGateway, GameStateGatewayImp)
    container.register(PlayerStateGateway, PlayerStateGatewayImp)
    container.register(GameStatesStorage, GameStatesStorageImpl)
    container.register(PlayerStatesStorage, PlayerStatesStorageImpl)
    container.register(HandlerUpdates, HandlerUpdates)
    container.register(RabbitMQPoller, build_poller(settings))
    container.register(Updates, Updates)


def build_poller(settings: Settings) -> RabbitMQPoller:
    return RabbitMQPoller(
        settings.rabbitmq.url,
        settings.rabbitmq.queue
    )

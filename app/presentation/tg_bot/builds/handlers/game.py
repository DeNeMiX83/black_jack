from sqlalchemy.ext.asyncio import AsyncSession
from app.di.container import Container
from app.infrastructure.store.sqlalchemy.gateway import (
    GameGatewayImpl,
    GameStateGatewayImpl,
    ChatGatewayImpl,
    CommiterImp,
)
from app.core.game.handlers import CreateGameHandler


def build(container: Container) -> None:
    container.register(CreateGameHandler, game_create)


def game_create(
    session: AsyncSession,
) -> CreateGameHandler:
    game_gateway = GameGatewayImpl(session)
    game_state_gateway = GameStateGatewayImpl(session)
    chat_gateway = ChatGatewayImpl(session)
    commiter = CommiterImp(session)
    return CreateGameHandler(
        game_gateway, game_state_gateway, chat_gateway, commiter
    )

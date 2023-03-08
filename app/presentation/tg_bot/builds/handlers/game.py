from sqlalchemy.ext.asyncio import AsyncSession
from app.di.container import Container
from app.infrastructure.store.sqlalchemy.gateway import (
    GameGatewayImpl,
    GameStateGatewayImpl,
    ChatGatewayImpl,
    PlayerGatewayImpl,
    UserGatewayImpl,
    CommiterImp,
)
from app.core.game.handlers import CreateGameAndGetHandler, AddPlayerHandler


def build(container: Container) -> None:
    container.register(CreateGameAndGetHandler, game_create)
    container.register(AddPlayerHandler, add_player)


def game_create(
    session: AsyncSession,
) -> CreateGameAndGetHandler:
    game_gateway = GameGatewayImpl(session)
    game_state_gateway = GameStateGatewayImpl(session)
    chat_gateway = ChatGatewayImpl(session)
    commiter = CommiterImp(session)
    return CreateGameAndGetHandler(
        game_gateway, game_state_gateway, chat_gateway, commiter
    )


def add_player(
    session: AsyncSession,
) -> AddPlayerHandler:
    game_gateway = GameGatewayImpl(session)
    player_gateway = PlayerGatewayImpl(session)
    user_gateway = UserGatewayImpl(session)
    chat_gateway = ChatGatewayImpl(session)
    commiter = CommiterImp(session)
    return AddPlayerHandler(
        game_gateway, player_gateway, user_gateway, chat_gateway, commiter
    )

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
from app.core.game.handlers import (
    CreateAndReturnGameHandler, AddPlayerHandler, GetGameByChatTgIdHandler,
    GetGamePlayersHandler, UpdateGameStateHandler, UpdatePlayerBetHandler,
    UpdatePlayerStateHandler
)


def build(container: Container) -> None:
    container.register(CreateAndReturnGameHandler, game_create)
    container.register(AddPlayerHandler, add_player)
    container.register(GetGameByChatTgIdHandler, get_game_by_chat_id)
    container.register(GetGamePlayersHandler, get_game_players)
    container.register(UpdateGameStateHandler, update_game_state)


def game_create(
    session: AsyncSession,
) -> CreateAndReturnGameHandler:
    game_gateway = GameGatewayImpl(session)
    game_state_gateway = GameStateGatewayImpl(session)
    chat_gateway = ChatGatewayImpl(session)
    commiter = CommiterImp(session)
    return CreateAndReturnGameHandler(
        game_gateway, game_state_gateway, chat_gateway, commiter
    )


def add_player(
    session: AsyncSession,
) -> AddPlayerHandler:
    game_gateway = GameGatewayImpl(session)
    player_gateway = PlayerGatewayImpl(session)
    user_gateway = UserGatewayImpl(session)
    commiter = CommiterImp(session)
    return AddPlayerHandler(
        game_gateway, player_gateway, user_gateway, commiter
    )


def get_game_by_chat_id(
    session: AsyncSession
) -> GetGameByChatTgIdHandler:
    game_gateway = GameGatewayImpl(session)
    chat_gateway = ChatGatewayImpl(session)
    return GetGameByChatTgIdHandler(game_gateway, chat_gateway)


def get_game_players(
    session: AsyncSession
) -> GetGamePlayersHandler:
    player_gateway = PlayerGatewayImpl(session)
    return GetGamePlayersHandler(player_gateway)


def update_game_state(
    session: AsyncSession,
) -> UpdateGameStateHandler:
    game_state_gateway = GameStateGatewayImpl(session)
    commiter = CommiterImp(session)
    return UpdateGameStateHandler(game_state_gateway, commiter)


def update_player_bet(
    session: AsyncSession,
) -> UpdatePlayerBetHandler:
    player_gateway = PlayerGatewayImpl(session)
    commiter = CommiterImp(session)
    return UpdatePlayerBetHandler(player_gateway, commiter)


def update_player_state(
    session: AsyncSession,
) -> UpdatePlayerStateHandler:
    player_gateway = PlayerGatewayImpl(session)
    commiter = CommiterImp(session)
    return UpdatePlayerStateHandler(player_gateway, commiter)

from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.store.sqlalchemy.gateway import (
    GameGatewayImpl,
    GameStateGatewayImpl,
    ChatGatewayImpl,
    PlayerGatewayImpl,
    UserGatewayImpl,
    PlayerCardsGatewayImpl,
    CommiterImp,
)
from app.core.game.handlers import (
    CreateAndReturnGameHandler, AddPlayerHandler, GetGameByChatTgIdHandler,
    GetGamePlayersHandler, UpdateGameStateHandler, UpdatePlayerBetHandler,
    UpdatePlayerStateHandler, GetCardHandler, GetPlayerHandler,
    GameOverHandler, DeletePlayerHandler, SavePlayerResultsHandler
)


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


def get_card(
    session: AsyncSession,
) -> GetCardHandler:
    player_gateway = PlayerGatewayImpl(session)
    player_cards_gateway = PlayerCardsGatewayImpl(session)
    commiter = CommiterImp(session)
    return GetCardHandler(player_gateway, player_cards_gateway, commiter)


def get_player(
    session: AsyncSession,
) -> GetPlayerHandler:
    player_gateway = PlayerGatewayImpl(session)
    return GetPlayerHandler(player_gateway)


def game_over_handler_build(
    session: AsyncSession,
) -> GameOverHandler:
    game_gateway = GameGatewayImpl(session)
    commiter = CommiterImp(session)
    return GameOverHandler(game_gateway, commiter)


def delete_player_by_id(
    session: AsyncSession,
) -> DeletePlayerHandler:
    player_gateway = PlayerGatewayImpl(session)
    commiter = CommiterImp(session)
    return DeletePlayerHandler(player_gateway, commiter)


def save_player_results(
    session: AsyncSession,
) -> SavePlayerResultsHandler:
    player_gateway = PlayerGatewayImpl(session)
    commiter = CommiterImp(session)
    return SavePlayerResultsHandler(player_gateway, commiter)

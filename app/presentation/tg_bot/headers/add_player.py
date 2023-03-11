from sqlalchemy.ext.asyncio import AsyncSession
from app.common.logger import logger
from app.infrastructure.tg_api import TgBot
from app.infrastructure.tg_api.dto import Update
from app.presentation.tg_bot.loader import tg_bot
from app.core.game.exceptions import (
    PlayerAlreadyExistsException
)
from app.infrastructure.tg_api.filters import GameStateFilter
from app.core.chat import dto as chat_dto
from app.core.game import dto as game_dto
from app.core.game import entities as game_entities
from app.core.game.handlers import AddPlayerHandler, GetGameByChatTgIdHandler
from app.presentation.tg_bot.builds.handlers import (
    add_player,
    get_game_by_chat_id
)


@tg_bot.callback_query_handler(
    GameStateFilter(game_entities.game_states.START)
)
async def _add_player(
    update: Update,
    session: AsyncSession,
    bot: TgBot
):
    add_player_handler = add_player(session)
    get_game_by_chat_tg_id_handler = get_game_by_chat_id(session)

    data = update.callback_query.data  # type: ignore
    if 'user_join_game' not in data:  # type: ignore
        return

    chat = chat_dto.Chat(
        tg_id=update.callback_query.message.chat.id,  # type: ignore
        name=update.callback_query.message.chat.title  # type: ignore
    )

    game = await get_game_by_chat_tg_id_handler.execute(chat)

    player_create = game_dto.PlayerCreate(
        tg_id=update.callback_query.from_user.id,  # type: ignore
        username=update.callback_query.from_user.username,  # type: ignore
        game_id=game.id
    )

    try:
        await add_player_handler.execute(player_create)
    except PlayerAlreadyExistsException:
        pass
    logger.info(f'{chat.tg_id}: user - {player_create.tg_id} added to game: {game.id}')

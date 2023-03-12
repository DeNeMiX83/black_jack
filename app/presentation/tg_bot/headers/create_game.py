from app.common.logger import logger
from app.presentation.tg_bot.states import (
    GameStates
)
from app.infrastructure.tg_api import TgBot
from app.infrastructure.tg_api.dto import Update
from app.infrastructure.tg_api.filters import CommandFilter
from app.presentation.tg_bot.loader import tg_bot
from app.core.game.exceptions import (
    ChatNotFoundException,
    GameAlreadyExistsException,
)
from app.core.game import dto as game_dto
from app.presentation.tg_bot.builds.handlers import (
    game_create
)


@tg_bot.message_handler(CommandFilter("/create_game"))
async def create_game(
    update: Update,
    bot: TgBot
):
    if update.callback_query is not None:
        chat_id = update.callback_query.message.chat.id
    else:
        chat_id = update.message.chat.id
        
    session = await bot.get_session()
    create_and_return_game_handler = game_create(session)

    game_states_storage = update.game_states_storage

    logger.info(f'{chat_id}: Создание игры')

    if update.message is None:
        return
    game_create_dto = game_dto.GameCreate(
        chat_tg_id=chat_id,
    )
    try:
        game = await create_and_return_game_handler.execute(game_create_dto)
    except ChatNotFoundException:
        await bot.send_message(
            chat_id=chat_id, text="Чат не найден, нажмите /start"
        )
        return
    except GameAlreadyExistsException:
        await bot.send_message(
            chat_id=chat_id, text="Игра уже существует"
        )
        return

    logger.info(f'{chat_id}: Игра создана')

    game_states_storage.add_state(
        chat_id,
        {
            'state': GameStates.PRE_START,
            'game_id': game.id,
        }
    )
    update.message.entities = None
    await bot.seng_update(update)

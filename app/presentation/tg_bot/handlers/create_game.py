import logging
from app.infrastructure.tg_api.states import (
    GameState,
    GameStateKey,
    GameStateData,
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
from app.presentation.tg_bot.builders import game_create
from app.presentation.tg_bot.middlewares import throttling_rate

logger = logging.getLogger()


@tg_bot.message_handler(CommandFilter("/game_create"))
async def create_game(update: Update, bot: TgBot):
    if update.callback_query is not None:
        chat_id = update.callback_query.message.chat.id
    else:
        chat_id = update.message.chat.id

    session = await bot.get_session()
    create_and_return_game_handler = game_create(session)

    game_states_storage = await bot.get_game_states_storage()

    logger.info(f"{chat_id}: Создание игры")

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
        await bot.send_message(chat_id=chat_id, text="Игра уже существует")
        return

    logger.info(f"{chat_id}: Игра создана")

    await game_states_storage.add_state(
        GameStateKey(chat_id=chat_id),
        GameStateData(state=GameState.PRE_START, game_id=game.id),
    )
    update.message.entities = None
    logger.info(f"{chat_id}: состояние игры стало {GameState.PRE_START}")
    await bot.seng_update(update)

import json
from app.common.logger import logger
from app.infrastructure.tg_api import TgBot
from app.infrastructure.tg_api.dto import Update
from app.infrastructure.tg_api.filters import CommandFilter
from app.presentation.tg_bot.loader import tg_bot
from app.core.game.exceptions import (
    ChatNotFoundException, GameAlreadyExistsException
)
from app.core.chat import dto as chat_dto
from app.core.game import dto as game_dto
from app.core.game.handlers import CreateGameHandler


@tg_bot.message_handler(CommandFilter('/create_game'))
async def create_game(update: Update, handler: CreateGameHandler, bot: TgBot):
    if update.message is None:
        return
    game_create = game_dto.GameCreate(
        chat=chat_dto.ChatCreate(
            tg_id=update.message.chat.id,
            name=update.message.chat.title
        )
    )

    try:
        await handler.execute(game_create)
    except ChatNotFoundException:
        await bot.send_message(
            chat_id=update.message.chat.id,
            text='Чат не найден, нажмите /start'
        )
        return
    except GameAlreadyExistsException:
        await bot.send_message(
            chat_id=update.message.chat.id,
            text='Игра уже существует'
        )
        return

    inline_keyboard = {
        "inline_keyboard": [
            [
                {"text": "Присоединиться", "callback_data": "user_join_game"},
            ]
        ]
    }
    await bot.send_message(
        chat_id=update.message.chat.id,
        text="Вы создали игру.",
        reply_markup=json.dumps(inline_keyboard)
    )
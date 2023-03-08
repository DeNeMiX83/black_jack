import json
import asyncio
from app.common.logger import logger
from app.infrastructure.tg_api import TgBot
from app.infrastructure.tg_api.dto import Update
from app.infrastructure.tg_api.filters import CommandFilter
from app.presentation.tg_bot.loader import tg_bot
from app.core.game.exceptions import (
    ChatNotFoundException,
    GameAlreadyExistsException,
)
from app.core.chat import dto as chat_dto
from app.core.game import dto as game_dto
from app.core.game.handlers import CreateGameAndGetHandler


@tg_bot.message_handler(CommandFilter("/create_game"))
async def create_game(
    update: Update, handler: CreateGameAndGetHandler, bot: TgBot
):
    if update.message is None:
        return
    game_create = game_dto.GameCreate(
        chat=chat_dto.ChatCreate(
            tg_id=update.message.chat.id, name=update.message.chat.title
        )
    )

    try:
        await handler.execute(game_create)
    except ChatNotFoundException:
        await bot.send_message(
            chat_id=update.message.chat.id, text="Чат не найден, нажмите /start"
        )
        return
    except GameAlreadyExistsException:
        await bot.send_message(
            chat_id=update.message.chat.id, text="Игра уже существует"
        )
        return

    inline_keyboard = {
        "inline_keyboard": [
            [
                {
                    "text": "Присоединиться",
                    "callback_data": "user_join_game_",
                },
            ]
        ]
    }

    time = 60
    msg = await bot.send_message(
        chat_id=update.message.chat.id,
        text=f"Начинаем набор игроков",
    )

    await bot.send_message(
        chat_id=update.message.chat.id,
        text="Нажмите кнопку ниже, чтобы участвовать.",
        reply_markup=json.dumps(inline_keyboard),
    )

    delta = 10
    for i in range(time, -1, -(delta)):
        await bot.edit_message_text(
            chat_id=update.message.chat.id,
            message_id=msg.message_id,
            text=f"Начинаем набор игроков.\nДо окончания сбора игроков осталось {i} секунд.",
        )
        await asyncio.sleep(delta)

    await bot.send_message(
        chat_id=update.message.chat.id, text="Начинаем игру."
    )
from app.presentation.tg_bot.loader import tg_bot
from app.infrastructure.tg_api import TgBot
from app.infrastructure.tg_api.dto import Update
from app.infrastructure.tg_api.filters import CommandFilter
from app.core.chat import dto as chat_dto
from app.presentation.tg_bot.builders import (
    chat_create,
)
from app.presentation.tg_bot.middlewares import throttling_rate


@throttling_rate(rate_limit=5)
@tg_bot.message_handler(CommandFilter("/start"))
async def add_new_chat(update: Update, bot: TgBot):
    chat_id = update.message.chat.id  # type: ignore

    session = await bot.get_session()
    chat_create_handler = chat_create(session)
    if update.message is None:
        return
    chat = chat_dto.ChatCreate(
        tg_id=chat_id, name=update.message.chat.title  # type: ignore
    )

    try:
        await chat_create_handler.execute(chat)
    except ValueError:
        await bot.send_message(
            chat_id=chat_id,
            text="Чат уже добавлен.\nВы можете создать игру в чате.\nДля этого нажмите /game_create",
        )
        return

    await bot.send_message(
        chat_id=chat_id,
        text="Приветствую! Вы можете создать игру в чате.\nДля этого нажмите /game_create",
    )

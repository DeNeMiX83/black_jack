from app.common.logger import logger
from app.presentation.tg_bot.loader import tg_bot
from app.infrastructure.tg_api import TgBot
from app.infrastructure.tg_api.dto import Update
from app.infrastructure.tg_api.filters import CommandFilter
from app.core.chat import dto as chat_dto
from app.core.chat.handlers import CreateChatHandler


@tg_bot.message_handler(CommandFilter('/start'))
async def add_new_chat(update: Update, handler: CreateChatHandler, bot: TgBot):
    if update.message is None:
        return
    chat = chat_dto.ChatCreate(
        tg_id=update.message.chat.id,
        name=update.message.chat.title
    )

    try:
        await handler.execute(chat)
    except ValueError:
        await bot.send_message(
            chat_id=chat.tg_id,
            text='Чат уже добавлен.\nВы можете создать игру в чате.\nДля этого нажмите /create_game'
        )
        return

    await bot.send_message(
        chat_id=update.message.chat.id,
        text='Приветствую! Вы можете создать игру в чате.\nДля этого нажмите /create_game'
    )

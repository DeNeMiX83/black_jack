from app.presentation.tg_bot.loader import tg_bot
from app.infrastructure.tg_api import TgBot
from app.infrastructure.tg_api.dto import Update
from app.infrastructure.tg_api.filters import CommandFilter


@tg_bot.message_handler(CommandFilter("/help"))
async def _get_user_balance(update: Update, bot: TgBot):
    chat_id = update.message.chat.id  # type: ignore

    text = '''
    🤖Команды:
    /help - получить справку.
    /start - начать взаимодействие с ботом.
    /create_game - создать игру.
    /balance - узнать свой баланс.
    '''

    await bot.send_message(
        chat_id=chat_id, text=text
    )

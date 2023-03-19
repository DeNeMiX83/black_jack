from app.presentation.tg_bot.loader import tg_bot
from app.infrastructure.tg_api import TgBot
from app.infrastructure.tg_api.dto import Update
from app.infrastructure.tg_api.filters import CommandFilter
from app.core.user.exceptions import UserNotFoundException
from app.presentation.tg_bot.builders import (
    get_user_balance_handler_build,
)
from app.presentation.tg_bot.middlewares import throttling_rate


@throttling_rate(rate_limit=5)
@tg_bot.message_handler(CommandFilter("/balance"))
async def _get_user_balance(update: Update, bot: TgBot):
    chat_id = update.message.chat.id  # type: ignore

    session = await bot.get_session()
    get_user_balance_handler = get_user_balance_handler_build(session)
    ans_text = f"Пользователь @{update.message.from_user.username}\n"

    try:
        balance = await get_user_balance_handler.execute(
            update.message.from_user.id
        )
    except UserNotFoundException:
        await bot.send_message(
            chat_id=chat_id,
            text=ans_text + "Нет данных",
        )
        return

    await bot.send_message(
        chat_id=chat_id, text=ans_text + f"Ваш баланс: {balance}"
    )

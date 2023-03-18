from app.presentation.tg_bot.loader import tg_bot
from app.infrastructure.tg_api import TgBot
from app.infrastructure.tg_api.dto import Update
from app.infrastructure.tg_api.filters import CommandFilter
from app.presentation.tg_bot.builders import (
    get_top_users_handler_build,
)


@tg_bot.message_handler(CommandFilter("/top"))
async def _get_top_users(update: Update, bot: TgBot):
    chat_id = update.message.chat.id  # type: ignore

    session = await bot.get_session()
    get_top_users_handler = get_top_users_handler_build(session)
    ans_text = "Топ пользователей\n"

    users = await get_top_users_handler.execute(10)

    await bot.send_message(
        chat_id=chat_id, text=ans_text + "\n".join(
            f"@{user.username}: {user.balance}" for user in users
        )
    )

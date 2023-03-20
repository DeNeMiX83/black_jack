from app.presentation.tg_bot.loader import tg_bot
from app.infrastructure.tg_api import TgBot
from app.infrastructure.tg_api.dto import Update
from app.infrastructure.tg_api.filters import CommandFilter
from app.core.user.exceptions import UserNotFoundException
from app.presentation.tg_bot.builders import (
    increase_user_balance_handler_build,
)
from app.presentation.tg_bot.middlewares import throttling_rate
from app.core.user import dto


@throttling_rate(rate_limit=5)
@tg_bot.message_handler(CommandFilter("/get_cache"))
async def _increase_balance(update: Update, bot: TgBot):
    chat_id = update.message.chat.id  # type: ignore
    user_id = update.message.from_user.id
    username = update.message.from_user.username

    session = await bot.get_session()
    increase_user_balance_handler = increase_user_balance_handler_build(session)
    try:
        result = await increase_user_balance_handler.execute(
            dto.IncreaseUserBalance(
                user_tg_id=user_id,
                size_increase=bot.settings.size_balance_increase
            )
        )
    except UserNotFoundException:
        return
    if result:
        await bot.send_message(
            chat_id=chat_id,
            text=f"@{username} баланс увеличен + {bot.settings.size_balance_increase}",
        )
    else:
        await bot.send_message(
            chat_id=chat_id,
            text=f"@{username} воспользоваться этой функцией могут только пользователи с нулевым балансом",
        )
    await session.close()

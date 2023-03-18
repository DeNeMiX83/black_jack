from app.presentation.tg_bot.loader import tg_bot
from app.infrastructure.tg_api import TgBot
from app.infrastructure.tg_api.dto import Update
from app.infrastructure.tg_api.filters import CommandFilter
from app.presentation.tg_bot.handlers.common import start_procces_game_over


@tg_bot.message_handler(CommandFilter("/game_stop"))
async def _game_stop(update: Update, bot: TgBot):
    await start_procces_game_over(update, bot)

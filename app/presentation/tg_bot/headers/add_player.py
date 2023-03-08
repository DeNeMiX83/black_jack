import json
import asyncio
from uuid import UUID
from app.common.logger import logger
from app.infrastructure.tg_api import TgBot
from app.infrastructure.tg_api.dto import Update
from app.presentation.tg_bot.loader import tg_bot
from app.core.game.exceptions import (
    PlayerAlreadyExistsException
)
from app.core.game import dto as game_dto
from app.core.game.handlers import AddPlayerHandler


@tg_bot.callback_query_handler()
async def add_player(update: Update, handler: AddPlayerHandler, bot: TgBot):
    data = update.callback_query.data  # type: ignore
    if 'user_join_game' not in data:  # type: ignore
        return

    player_create = game_dto.PlayerCreate(
        tg_id=update.callback_query.from_user.id,  # type: ignore
        username=update.callback_query.from_user.username,  # type: ignore
        chat_id=update.callback_query.message.chat.id  # type: ignore
    )

    try:
        await handler.execute(player_create)
    except PlayerAlreadyExistsException:
        return

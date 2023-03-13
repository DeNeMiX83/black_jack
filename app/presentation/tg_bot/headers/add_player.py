import json
import asyncio
from uuid import UUID
from app.common.logger import logger
from app.infrastructure.tg_api import TgBot
from app.infrastructure.tg_api.dto import Update
from app.presentation.tg_bot.loader import tg_bot
from app.core.game.exceptions import PlayerAlreadyExistsException
from app.presentation.tg_bot.states import GameStates
from app.infrastructure.tg_api.filters import (
    GameStateFilter,
    CallbackQueryDataFilter,
)
from app.core.chat import dto as chat_dto
from app.core.game import dto as game_dto
from app.core.game import entities as game_entities
from app.presentation.tg_bot.builds.handlers import (
    add_player,
)
from app.presentation.tg_bot.builds.handlers import (
    update_game_state,
    get_game_players,
)
from app.presentation.tg_bot.headers.utils import start_procces_game_over


@tg_bot.callback_query_handler(
    GameStateFilter(GameStates.START),
    CallbackQueryDataFilter("user_join_game")
)
async def _add_player(update: Update, bot: TgBot):
    chat_id = update.callback_query.message.chat.id

    session = await bot.get_session()
    add_player_handler = add_player(session)
    game_states_storage = update.game_states_storage

    game_data = game_states_storage.get_state(chat_id)
    game_id = game_data["game_id"]

    chat = chat_dto.Chat(
        tg_id=chat_id,  # type: ignore
        name=update.callback_query.message.chat.title,  # type: ignore
    )

    player_create = game_dto.PlayerCreate(
        tg_id=update.callback_query.from_user.id,  # type: ignore
        username=update.callback_query.from_user.username,  # type: ignore
        game_id=game_id,
    )

    try:
        await add_player_handler.execute(player_create)
    except PlayerAlreadyExistsException:
        return

    logger.info(
        f"{chat.tg_id}: user - {player_create.tg_id} added to game: {game_id}"
    )


@tg_bot.common_handler(GameStateFilter(GameStates.PRE_START))
async def gathering_players(update: Update, bot: TgBot):
    if update.callback_query is not None:
        chat_id = update.callback_query.message.chat.id
    else:
        chat_id = update.message.chat.id

    game_states_storage = update.game_states_storage
    game_data = game_states_storage.get_state(chat_id)
    game_id = game_data["game_id"]

    game_states_storage.add_state(
        chat_id,
        {
            "state": GameStates.START,
            "game_id": game_id,
        },
    )

    await timer_waiting_moves(update, bot, game_id)

    await game_start(update, bot)

    await set_states(update, bot)

    await bot.seng_update(update)


async def timer_waiting_moves(update: Update, bot: TgBot, game_id: UUID):
    if update.callback_query is not None:
        chat_id = update.callback_query.message.chat.id
    else:
        chat_id = update.message.chat.id

    inline_keyboard = {
        "inline_keyboard": [
            [
                {
                    "text": "Присоединиться к игре",
                    "callback_data": "user_join_game",
                },
            ]
        ]
    }

    time = 10
    delta = 10

    game_states_storage = update.game_states_storage
    game_states_storage.add_state(
        chat_id,
        {
            "state": GameStates.START,
            "game_id": game_id,
        },
    )

    logger.info(f"{chat_id}: Сбор участников")

    inline_keyboard = {
        "inline_keyboard": [
            [
                {
                    "text": "Присоединиться к игре",
                    "callback_data": "user_join_game",
                },
            ]
        ]
    }

    time = 10
    delta = 10
    msg = await bot.send_message(
        chat_id=chat_id,
        text="Начинаем набор игроков\n" +
             f"До окончания сбора игроков осталось {time} секунд.",
        reply_markup=json.dumps(inline_keyboard),
    )
    await asyncio.sleep(delta)

    for i in range(time - delta, -1, -(delta)):
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=msg.message_id,
            text="Начинаем набор игроков.\n" +
                 f"До окончания сбора игроков осталось {i} секунд.",
            reply_markup=json.dumps(inline_keyboard),
        )
        if i > 0:
            await asyncio.sleep(delta)


async def game_start(update: Update, bot: TgBot):
    if update.callback_query is not None:
        chat_id = update.callback_query.message.chat.id
    else:
        chat_id = update.message.chat.id

    session = await bot.get_session()
    get_players_handler = get_game_players(session)
    game_states_storage = update.game_states_storage

    game_data = game_states_storage.get_state(chat_id)
    game_id = game_data["game_id"]

    logger.info(f"{chat_id}: Запуск игры")

    await bot.send_message(chat_id=chat_id, text="Начинаем игру.")

    players: list[game_entities.Player] = await get_players_handler.execute(
        game_id
    )  # type: ignore

    if not players:
        await bot.send_message(chat_id=chat_id, text="Нет участников")
        await start_procces_game_over(update, bot)
        return

    await bot.send_message(
        chat_id=chat_id, text=get_text_list_players(players)
    )


def get_text_list_players(players: list[game_entities.Player]) -> str:
    return "\n".join(
        f"{n + 1}. @{player.user.username}" for n, player in enumerate(players)
    )


async def set_states(
    update: Update, bot: TgBot
):
    if update.callback_query is not None:
        chat_id = update.callback_query.message.chat.id
    else:
        chat_id = update.message.chat.id

    session = await bot.get_session()

    update_game_state_handler = update_game_state(session)

    game_states_storage = update.game_states_storage

    game_data = game_states_storage.get_state(chat_id)
    game_id = game_data["game_id"]

    new_game_state = game_dto.GameStateUpdate(
        game_id=game_id,
        new_state=game_entities.game_states.BET,
    )

    await update_game_state_handler.execute(new_game_state)

    game_states_storage.add_state(
        chat_id,
        {
            "state": GameStates.PRE_BET,
            "game_id": game_id,
        },
    )

    logger.info(
        f"{chat_id}: Состояние игры изменилось на {new_game_state.new_state}"
    )

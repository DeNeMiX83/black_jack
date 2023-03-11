import json
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.common.logger import logger
from app.presentation.tg_bot.states import GameStatesStorage, PlayerStatesStorage
from app.infrastructure.tg_api import TgBot
from app.infrastructure.tg_api.dto import Update
from app.infrastructure.tg_api.filters import CommandFilter
from app.presentation.tg_bot.loader import tg_bot
from app.core.game.exceptions import (
    ChatNotFoundException,
    GameAlreadyExistsException,
)
from app.core.game import dto as game_dto
from app.core.game import entities as game_entities
from app.presentation.tg_bot.builds.handlers import (
    game_create, update_game_state, get_game_players,
    game_over
)
from app.presentation.tg_bot.headers.utils import start_procces_game_over
from app.presentation.tg_bot.headers.get_bet import bet_transfer_stroke


@tg_bot.message_handler(CommandFilter("/create_game"))
async def create_game(
    update: Update,
    session: AsyncSession,
    game_states_storage: GameStatesStorage,
    bot: TgBot
):
    create_and_return_game_handler = game_create(session)
    chat_id = update.message.chat.id  # type: ignore
    # Создание игры

    logger.info(f'{chat_id}: Создание игры')

    if update.message is None:
        return
    game_create_dto = game_dto.GameCreate(
        chat_tg_id=chat_id,
    )
    try:
        game = await create_and_return_game_handler.execute(game_create_dto)
    except ChatNotFoundException:
        await bot.send_message(
            chat_id=chat_id, text="Чат не найден, нажмите /start"
        )
        return
    except GameAlreadyExistsException:
        await bot.send_message(
            chat_id=chat_id, text="Игра уже существует"
        )
        return

    logger.info(f'{chat_id}: Игра создана')

    game_states_storage.add_state(
        chat_id,
        {
            'state': game_entities.game_states.START,
            'game_id': game.id,
        }
    )

    # Сбор участников

    await gathering_players(update, bot)


async def gathering_players(update: Update, bot: TgBot):
    chat_id = update.message.chat.id  # type: ignore

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
        chat_id=update.message.chat.id,
        text=f"Начинаем набор игроков\nДо окончания сбора игроков осталось {time} секунд.",
        reply_markup=json.dumps(inline_keyboard)
    )
    await asyncio.sleep(delta)

    for i in range(time-delta, -1, -(delta)):
        await bot.edit_message_text(
            chat_id=update.message.chat.id,
            message_id=msg.message_id,
            text=f"Начинаем набор игроков.\nДо окончания сбора игроков осталось {i} секунд.",
            reply_markup=json.dumps(inline_keyboard)
        )
        if i > 0:
            await asyncio.sleep(delta)

    # Запуск игры

    await game_start(update, bot)


async def game_start(update: Update, bot: TgBot):
    chat_id = update.message.chat.id  # type: ignore

    session = await bot.get_session()

    update_game_state_handler = update_game_state(session)
    game_over_handler = game_over(session)
    get_players_handler = get_game_players(session)

    game_states_storage = update.game_states_storage
    player_states_storage = update.player_states_storage

    game_data = game_states_storage.get_state(chat_id)
    game_id = game_data['game_id']

    chat_id = update.message.chat.id

    logger.info(f"{chat_id}: Запуск игры")

    await bot.send_message(
        chat_id=update.message.chat.id, text="Начинаем игру."
    )

    players: list[game_entities.Player] = (
        await get_players_handler.execute(game_id)  # type: ignore
    )

    if players:
        text_players = '\n'.join(f'{n + 1}. @{player.user.username}' for n, player in enumerate(players))
    else:
        await bot.send_message(
            chat_id=update.message.chat.id,
            text="Нет участников"
        )
        await start_procces_game_over(
            update,
            bot,
            game_states_storage,
            update_game_state_handler,
            game_over_handler,
        )
        return

    await bot.send_message(
        chat_id=update.message.chat.id,
        text=text_players
    )

    if not players:
        logger.info(f"{chat_id}: Участников нету, игра завершена")
        return

    new_game_state = game_dto.GameStateUpdate(
        game_id=game_id,
        new_state=game_entities.game_states.BET,
    )

    await update_game_state_handler.execute(new_game_state)

    game_states_storage.add_state(
        update.message.chat.id,
        {
            'state': new_game_state.new_state,
            'game_id': game_id,
        }
    )

    logger.info(f"{chat_id}: Состояние игры изменилось на {new_game_state.new_state}")

    for player in players:
        player_states_storage.add_state(
            (player.game.chat.tg_id, player.user.tg_id),
            {
                'state': game_entities.player_status.PLAYING,
                'player_id': player.id,
            }
        )
        logger.info(f"{chat_id}: Состояние игрока изменилось на {game_entities.player_status.PLAYING}")

    # Сбор ставок

    await bet_transfer_stroke(update, players, bot)

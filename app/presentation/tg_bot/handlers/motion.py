import json
import asyncio
from random import randrange
import logging
from app.infrastructure.tg_api import TgBot
from app.infrastructure.tg_api.dto import Update
from app.presentation.tg_bot.loader import tg_bot
from app.presentation.tg_bot.handlers.common import start_procces_game_over
from app.infrastructure.tg_api.states import (
    GameState,
    GameStateKey,
    GameStateData,
    PlayerState,
    PlayerStateKey,
    PlayerStateData,
)
from app.infrastructure.tg_api.filters import (
    GameStateFilter,
    PlayerStateFilter,
    CallbackQueryDataFilter,
)
from app.core.game import dto as game_dto
from app.core.game import entities as game_entities
from app.presentation.tg_bot.builders import (
    update_player_state,
    get_game_players,
    get_card,
    get_player,
    save_player_results,
)
from app.core.game import entities as game_entities

logger = logging.getLogger()


@tg_bot.callback_query_handler(
    GameStateFilter(GameState.MOTION),
    PlayerStateFilter(PlayerState.MOTION),
    CallbackQueryDataFilter("player_get_card"),
)
async def _get_card(update: Update, bot: TgBot):
    chat_id = update.callback_query.message.chat.id
    user_id = update.callback_query.from_user.id

    session = await bot.get_session()
    get_card_handler = get_card(session)
    get_player_handler = get_player(session)
    update_player_state_handler = update_player_state(session)
    player_states_storage = await bot.get_player_states_storage()

    player_data = update.player_state_data
    player_id = player_data.player_id

    card = await get_card_handler.execute(player_id)
    player = await get_player_handler.execute(player_id)

    await bot.delete_message(
        chat_id=chat_id,
        message_id=update.callback_query.message.message_id,
    )
    await bot.send_message(
        chat_id=chat_id,
        text=f"@{player.user.username} вытянул карту {card.rank}{card.suit}.\n"
        + f"Cчет: {player.score}",
    )

    if player.score > 21:
        await bot.send_message(
            chat_id=chat_id,
            text=f"@{player.user.username} набрал больше 21.",
        )
        await player_lose(update, bot)
        return

    new_state = game_dto.PlayerStateUpdate(
        player_id=player_id, new_state=game_entities.player_status.WAIT
    )
    await update_player_state_handler.execute(new_state)
    await player_states_storage.add_state(
        PlayerStateKey(chat_id=chat_id, user_id=user_id),
        PlayerStateData(state=PlayerState.WAIT, player_id=player_id),
    )

    logger.info(f"{chat_id}: user {user_id}: взял карту {card.rank}")
    await session.close()


@tg_bot.callback_query_handler(
    GameStateFilter(GameState.MOTION),
    PlayerStateFilter(PlayerState.MOTION),
    CallbackQueryDataFilter("player_pass"),
)
async def _motion_pass(update: Update, bot: TgBot):
    chat_id = update.callback_query.message.chat.id
    user_id = update.callback_query.from_user.id

    session = await bot.get_session()
    update_player_state_handler = update_player_state(session)
    player_states_storage = await bot.get_player_states_storage()

    player_data = update.player_state_data
    player_id = player_data.player_id

    await bot.delete_message(
        chat_id=chat_id,
        message_id=update.callback_query.message.message_id,
    )
    await bot.send_message(
        chat_id=chat_id,
        text=f"@{update.callback_query.from_user.username} пасанул",
    )

    new_state = game_dto.PlayerStateUpdate(
        player_id=player_id, new_state=game_entities.player_status.SKIP
    )

    await update_player_state_handler.execute(new_state)
    await player_states_storage.add_state(
        PlayerStateKey(chat_id=chat_id, user_id=user_id),
        PlayerStateData(state=PlayerState.SKIP, player_id=player_id),
    )

    logger.info(f"{chat_id}: user {user_id}: пропуск хода")
    await session.close()


@tg_bot.common_handler(GameStateFilter(GameState.PRE_MOTION))
async def motion_transfer_stroke(update: Update, bot: TgBot):
    if update.callback_query is not None:
        chat_id = update.callback_query.message.chat.id
    else:
        chat_id = update.message.chat.id

    game_states_storage = await bot.get_game_states_storage()

    game_data = update.game_state_data
    game_id = game_data.game_id

    await game_states_storage.add_state(
        GameStateKey(chat_id=chat_id),
        GameStateData(state=GameState.MOTION, game_id=game_id),
    )
    await timer_waiting_moves(update, bot)

    await start_procces_game_over(update, bot)

    await save_game_results(update, bot)


async def timer_waiting_moves(update: Update, bot: TgBot):
    if update.callback_query is not None:
        chat_id = update.callback_query.message.chat.id
    else:
        chat_id = update.message.chat.id

    session = await bot.get_session()

    get_players_handler = get_game_players(session)
    player_states_storage = await bot.get_player_states_storage()

    game_data = update.game_state_data
    game_id = game_data.game_id
    players: list[game_entities.Player] = await get_players_handler.execute(
        game_id
    )  # type: ignore
    await session.close()
    while players:
        for i in range(len(players)):
            player = players[i]
            await player_states_storage.add_state(
                PlayerStateKey(chat_id=chat_id, user_id=player.user.tg_id),
                PlayerStateData(state=PlayerState.MOTION, player_id=player.id),
            )
            inline_keyboard = {
                "inline_keyboard": [
                    [
                        {
                            "text": "Взять карту",
                            "callback_data": "player_get_card",
                        },
                        {
                            "text": "Пас",
                            "callback_data": "player_pass",
                        },
                    ]
                ]
            }
            await bot.send_message(
                chat_id=chat_id,
                text=f"@{player.user.username} сделайте ход\n"
                + f"Ваш счет: {player.score}",
                reply_markup=json.dumps(inline_keyboard),
            )
            await asyncio.sleep(10)

            player_state_data = await player_states_storage.get_state(
                PlayerStateKey(chat_id=chat_id, user_id=player.user.tg_id)
            )

            if player_state_data.state == PlayerState.MOTION:
                await bot.send_message(
                    chat_id=chat_id,
                    text=f"@{player.user.username} неуспел сделать ход",
                )
                await player_lose(update, bot)

        session = await bot.get_session()
        get_players_handler = get_game_players(session)

        players = await get_players_handler.execute(game_id)  # type: ignore
        players = list(
            filter(
                lambda player: player.status
                == game_entities.player_status.WAIT,
                players,
            )
        )
        await session.close()


async def save_game_results(update: Update, bot: TgBot):
    if update.callback_query is not None:
        chat_id = update.callback_query.message.chat.id
    else:
        chat_id = update.message.chat.id
    logger.info(f"{chat_id} подсчет результатов")

    session = await bot.get_session()

    get_players_handler = get_game_players(session)

    game_data = update.game_state_data
    game_id = game_data.game_id

    players: list[game_entities.Player] = await get_players_handler.execute(
        game_id
    )  # type: ignore

    dealer_result = randrange(14, 25)

    text = f"Дилер: {dealer_result}\n"
    lose = []
    win = []
    draw = []
    for n, player in enumerate(players):
        if player.status == game_entities.player_status.LOSE:
            text += (
                f"{n + 1}. @{player.user.username} \t проиграл\n"
                + f"счет: {player.score}\n"
            )
            lose.append(player.id)
        elif dealer_result > 21:
            text += (
                f"{n + 1}. @{player.user.username} \t выйграл\n"
                + f"счет: {player.score}\n"
            )
            win.append(player.id)
        elif player.score < dealer_result:
            text += (
                f"{n + 1}. @{player.user.username} \t проиграл\n"
                + f"счет: {player.score}\n"
            )
            lose.append(player.id)
        elif player.score == dealer_result:
            text += (
                f"{n + 1}. @{player.user.username} \t ничья\n"
                + f"счет: {player.score}\n"
            )
            draw.append(player.id)
        else:
            text += (
                f"{n + 1}. @{player.user.username} \t выйграл\n"
                + f"счет: {player.score}\n"
            )
            win.append(player.id)

    results = []
    for player_id in lose:
        logger.info(
            f"{chat_id}: {player.user.tg_id} выйграл ставка: {player.bet} прибавка: {0}"
        )
        new_result = game_dto.PlayerResult(
            player_id=player_id,
            new_state=game_entities.player_status.LOSE,
            winning=0,
        )

        results.append(new_result)
    for player_id in win:
        logger.info(
            f"{chat_id}: {player.user.tg_id} выйграл ставка: {player.bet} прибавка: {player.bet * 2}"
        )
        new_result = game_dto.PlayerResult(
            player_id=player_id,
            new_state=game_entities.player_status.WIN,
            winning=player.bet * 2,
        )
        results.append(new_result)
    for player_id in draw:
        logger.info(
            f"{chat_id}: {player.user.tg_id} выйграл ставка: {player.bet} прибавка: {player.bet * 1.5}"
        )
        new_result = game_dto.PlayerResult(
            player_id=player_id,
            new_state=game_entities.player_status.DRAW,
            winning=player.bet * 1.5,
        )
        results.append(new_result)

    logger.info(f"{chat_id} сохранение рузультатов в бд")
    save_player_results_handler = save_player_results(session)
    await save_player_results_handler.execute(results)

    await bot.send_message(
        chat_id=chat_id,
        text=text,
    )

    logger.info("Результаты подсчитаны")
    await session.close()


async def player_lose(update: Update, bot: TgBot):
    if update.callback_query is not None:
        chat_id = update.callback_query.message.chat.id
        user_id = update.callback_query.from_user.id
        username = update.callback_query.from_user.username
    else:
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        username = update.message.from_user.username

    session = await bot.get_session()
    update_player_state_handler = update_player_state(session)
    player_states_storage = await bot.get_player_states_storage()

    player_data = update.player_state_data
    player_id = player_data.player_id

    await player_states_storage.add_state(
        PlayerStateKey(chat_id=chat_id, user_id=user_id),
        PlayerStateData(state=PlayerState.LOSE, player_id=player_id),
    )
    new_state = game_dto.PlayerStateUpdate(
        player_id=player_id, new_state=game_entities.player_status.LOSE
    )
    await update_player_state_handler.execute(new_state)
    await bot.send_message(
        chat_id=chat_id,
        text=f"@{username} проиграл",
    )
    logger.info(f"{chat_id}: user {user_id} проиграл")
    await session.close()

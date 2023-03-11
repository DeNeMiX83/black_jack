import json
import asyncio
from random import randrange
from sqlalchemy.ext.asyncio import AsyncSession
from app.common.logger import logger
from app.infrastructure.tg_api import TgBot
from app.infrastructure.tg_api.dto import Update
from app.presentation.tg_bot.loader import tg_bot
from app.presentation.tg_bot.states import (
    GameStatesStorage,
    GameStates,
    PlayerStatesStorage,
)
from app.infrastructure.tg_api.filters import (
    GameStateFilter,
    PlayerStateFilter,
    CallbackQueryDataFilter,
)
from app.core.game import dto as game_dto
from app.core.game import entities as game_entities
from app.presentation.tg_bot.builds.handlers import (
    update_player_state,
    get_game_players,
    get_card,
    get_player,
    save_player_results,
)
from app.presentation.tg_bot.headers.utils import start_procces_game_over


@tg_bot.callback_query_handler(
    GameStateFilter(GameStates.MOTION),
    PlayerStateFilter(game_entities.player_status.MOTION),
    CallbackQueryDataFilter("player_get_card"),
)
async def _get_card(update: Update, session: AsyncSession, bot: TgBot):
    chat_id = update.callback_query.message.chat.id
    user_id = update.callback_query.from_user.id

    get_card_handler = get_card(session)
    get_player_handler = get_player(session)
    update_player_state_handler = update_player_state(session)
    player_states_storage = update.player_states_storage

    player_data = player_states_storage.get_state((chat_id, user_id))
    player_id = player_data["player_id"]

    card = await get_card_handler.execute(player_id)
    player = await get_player_handler.execute(player_id)

    await bot.send_message(
        chat_id=chat_id,
        text=f"@{player.user.username} вытянул карту {card.rank}.\n"
        + f"Cчет: {player.score}",
    )

    if player.score > 21:
        new_state = game_dto.PlayerStateUpdate(
            player_id=player_id, new_state=game_entities.player_status.LOSE
        )
        await bot.send_message(
            chat_id=chat_id,
            text=f"@{player.user.username} проиграл",
        )
        logger.info(f"{chat_id}: user {player.user.tg_id} проиграл")
    else:
        new_state = game_dto.PlayerStateUpdate(
            player_id=player_id, new_state=game_entities.player_status.PLAYING
        )

    await update_player_state_handler.execute(new_state)
    player_states_storage.add_state(
        (chat_id, user_id),
        {
            "state": new_state.new_state,
            "player_id": player_id,
        },
    )

    logger.info(f"{chat_id}: user {user_id}: взял карту {card.rank}")


@tg_bot.callback_query_handler(
    GameStateFilter(GameStates.MOTION),
    PlayerStateFilter(game_entities.player_status.MOTION),
    CallbackQueryDataFilter("player_pass"),
)
async def _motion_pass(update: Update, session: AsyncSession, bot: TgBot):
    chat_id = update.callback_query.message.chat.id
    user_id = update.callback_query.from_user.id

    update_player_state_handler = update_player_state(session)
    player_states_storage: PlayerStatesStorage = update.player_states_storage

    player_data = player_states_storage.get_state((chat_id, user_id))
    player_id = player_data["player_id"]

    await bot.send_message(
        chat_id=chat_id,
        text=f"@{update.callback_query.from_user.username} пасанул",
    )

    new_state = game_dto.PlayerStateUpdate(
        player_id=player_id, new_state=game_entities.player_status.SKIP
    )

    await update_player_state_handler.execute(new_state)
    player_states_storage.add_state(
        (chat_id, user_id),
        {
            "state": new_state.new_state,
            "player_id": player_id,
        },
    )

    logger.info(f"{chat_id}: user {user_id}: пропуск хода")


@tg_bot.common_handler(GameStateFilter(GameStates.PRE_MOTION))
async def motion_transfer_stroke(update: Update, bot: TgBot):
    if update.callback_query is not None:
        chat_id = update.callback_query.message.chat.id
    else:
        chat_id = update.message.chat.id

    session = await bot.get_session()
    update_player_state_handler = update_player_state(session)
    get_players_handler = get_game_players(session)

    game_states_storage: GameStatesStorage = update.game_states_storage
    player_states_storage: PlayerStatesStorage = update.player_states_storage

    game_data = game_states_storage.get_state(chat_id)
    game_id = game_data["game_id"]

    game_states_storage.add_state(
        chat_id,
        {
            "state": GameStates.MOTION,
            "game_id": game_id,
        },
    )

    players: list[game_entities.Player] = await get_players_handler.execute(
        game_id
    )  # type: ignore
    while players:
        for i in range(len(players)):
            player = players[i]
            new_state = game_dto.PlayerStateUpdate(
                player_id=player.id,
                new_state=game_entities.player_status.MOTION,
            )
            await update_player_state_handler.execute(new_state)
            player_states_storage.add_state(
                (chat_id, player.user.tg_id),
                {"state": new_state.new_state, "player_id": player.id},
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
            await asyncio.sleep(5)

        session = await bot.get_session()
        get_players_handler = get_game_players(session)

        players: list[game_entities.Player] = await get_players_handler.execute(
            game_id
        )  # type: ignore
        players = list(
            filter(
                lambda player: player.status
                == game_entities.player_status.PLAYING,
                players,
            )
        )

    await start_procces_game_over(update, bot)
    players: list[game_entities.Player] = await get_players_handler.execute(
        game_id
    )  # type: ignore

    logger.info("Подсчет результатов")

    session = await bot.get_session()
    update_player_state_handler = update_player_state(session)
    dealer_result = randrange(14, 25)

    text = f"Дилер: {dealer_result}\n"
    lose = []
    win = []
    draw = []
    for n, player in enumerate(players):
        if player.status == game_entities.player_status.LOSE:
            text += f"{n + 1}. @{player.user.username} \t проиграл счет: {player.score}\n"
            lose.append(player.id)
        elif dealer_result > 21:
            text += f"{n + 1}. @{player.user.username} \t выйграл счет: {player.score}\n"
            win.append(player.id)
        elif player.score < dealer_result:
            text += f"{n + 1}. @{player.user.username} \t проиграл счет: {player.score}\n"
            lose.append(player.id)
        elif player.score == dealer_result:
            text += f"{n + 1}. @{player.user.username} \t ничья счет: {player.score}\n"
            draw.append(player.id)
        else:
            text += f"{n + 1}. @{player.user.username} \t выйграл счет: {player.score}\n"
            win.append(player.id)

    results = []
    for player_id in lose:
        new_result = game_dto.PlayerResult(
            player_id=player_id,
            new_state=game_entities.player_status.LOSE,
            winning=0
        )

        results.append(new_result)
    for player_id in win:
        new_result = game_dto.PlayerResult(
            player_id=player_id,
            new_state=game_entities.player_status.WIN,
            winning=player.bet * 2
        )
        results.append(new_result)
    for player_id in draw:
        new_result = game_dto.PlayerResult(
            player_id=player_id,
            new_state=game_entities.player_status.DRAW,
            winning=player.bet * 1.5
        )
        results.append(new_result)

    save_player_results_handler = save_player_results(session)
    await save_player_results_handler.execute(results)

    await bot.send_message(
        chat_id=chat_id,
        text=text,
    )

    logger.info("Результаты подсчитаны")

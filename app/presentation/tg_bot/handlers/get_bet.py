import asyncio
import logging
from app.infrastructure.tg_api import TgBot
from app.infrastructure.tg_api.dto import Update
from app.presentation.tg_bot.loader import tg_bot
from app.infrastructure.tg_api.states import (
    GameState,
    GameStateKey,
    GameStateData,
    PlayerState,
    PlayerStateKey,
    PlayerStateData,
)
from app.infrastructure.tg_api.filters import (
    GameStateFilter, PlayerStateFilter
)
from app.core.game import dto as game_dto
from app.core.game import entities as game_entities
from app.presentation.tg_bot.builders import (
    update_player_bet,
    update_player_state,
    get_game_players,
    update_game_state,
    get_player,
    delete_player_by_id,
)
from app.presentation.tg_bot.handlers.common import start_procces_game_over

logger = logging.getLogger()


@tg_bot.message_handler(
    GameStateFilter(GameState.BET),
    PlayerStateFilter(PlayerState.BET),
)
async def _get_bet(update: Update, bot: TgBot):
    chat_id = update.message.chat.id
    user_id = update.message.from_user.id

    session = await bot.get_session()
    update_player_bet_handler = update_player_bet(session)
    update_player_state_handler = update_player_state(session)
    player_states_storage = await bot.get_player_states_storage()

    bet = update.message.text  # type: ignore

    try:
        bet = int(bet)
    except ValueError:
        await bot.send_message(chat_id=chat_id, text="Должны быть цифры")
        return

    int_32 = 2**31
    if bet >= int_32:
        await bot.send_message(
            chat_id=chat_id, text=f"Число должно быть меньше {int_32}"
        )
        return
    if bet <= 0:
        await bot.send_message(
            chat_id=chat_id, text="Число должно быть больше 0"
        )
        return

    player_data = update.player_state_data
    player_id = player_data.player_id

    bet_dto = game_dto.Bet(player_id=player_id, bet=bet)

    try:
        await update_player_bet_handler.execute(bet_dto)
    except ValueError:
        await bot.send_message(
            chat_id=chat_id, text="Некорректная сумма ставки"
        )
        return

    new_state = game_dto.PlayerStateUpdate(
        player_id=player_id, new_state=game_entities.player_status.WAIT
    )
    await update_player_state_handler.execute(new_state)
    await player_states_storage.add_state(
        PlayerStateKey(chat_id=chat_id, user_id=user_id),
        PlayerStateData(state=PlayerState.WAIT, player_id=player_id),
    )

    logger.info(f"{chat_id}: user {user_id}: сделал ставку: {bet}")
    logger.info(
        f"{chat_id}: user {user_id}: состояние сменилось "
        + f"на {PlayerState.WAIT}"
    )
    await session.close()


@tg_bot.common_handler(GameStateFilter(GameState.PRE_BET))
async def bet_transfer_stroke(update: Update, bot: TgBot):
    if update.callback_query is not None:
        chat_id = update.callback_query.message.chat.id
    else:
        chat_id = update.message.chat.id
    logger.info(f"{chat_id}: Начало принятия ставок")

    session = await bot.get_session()
    get_players_handler = get_game_players(session)
    game_states_storage = await bot.get_game_states_storage()

    game_data = update.game_state_data
    game_id = game_data.game_id

    await game_states_storage.add_state(
        GameStateKey(chat_id=chat_id),
        GameStateData(state=GameState.BET, game_id=game_id),
    )

    await timer_waiting_moves(update, bot)

    session = await bot.get_session()
    get_players_handler = get_game_players(session)
    players: list[game_entities.Player] = await get_players_handler.execute(
        game_id
    )  # type: ignore

    if not players:
        await bot.send_message(chat_id=chat_id, text="Нет участников")
        await start_procces_game_over(update, bot)
        return

    text = "\n".join(
        f"{n + 1}. @{player.user.username} - {player.bet}"
        for n, player in enumerate(players)
    )
    await bot.send_message(chat_id=chat_id, text="Все ставки приняты\n" + text)

    logger.info(f"{chat_id}: Все ставки приняты")

    await set_state(update, bot)

    await bot.seng_update(update)


async def timer_waiting_moves(update: Update, bot: TgBot):
    if update.callback_query is not None:
        chat_id = update.callback_query.message.chat.id
    else:
        chat_id = update.message.chat.id

    session = await bot.get_session()
    get_players_handler = get_game_players(session)
    update_player_state_handler = update_player_state(session)
    delete_player_by_id_handler = delete_player_by_id(session)
    player_states_storage = await bot.get_player_states_storage()

    game_data = update.game_state_data
    game_id = game_data.game_id

    players: list[game_entities.Player] = await get_players_handler.execute(
        game_id
    )

    for player in players:
        new_state = game_dto.PlayerStateUpdate(
            player_id=player.id, new_state=game_entities.player_status.BET
        )
        await update_player_state_handler.execute(new_state)
        await player_states_storage.add_state(
            PlayerStateKey(chat_id=chat_id, user_id=player.user.tg_id),
            PlayerStateData(state=PlayerState.BET, player_id=player.id),
        )
        await bot.send_message(
            chat_id=chat_id,
            text=f"@{player.user.username} введите ставку\n"
            + f"Баланс: {player.user.balance}",
        )
        await asyncio.sleep(15)

        session = await bot.get_session()
        get_player_handler = get_player(session)
        current_player = await get_player_handler.execute(player.id)
        if current_player.bet == 0:
            await bot.send_message(
                chat_id=chat_id,
                text=f"@{player.user.username} нет ставки. Удален из игры",
            )
            await delete_player_by_id_handler.execute(current_player.id)


async def set_state(update: Update, bot: TgBot):
    if update.callback_query is not None:
        chat_id = update.callback_query.message.chat.id
    else:
        chat_id = update.message.chat.id

    session = await bot.get_session()
    update_game_state_handler = update_game_state(session)
    game_states_storage = await bot.get_game_states_storage()

    game_data = update.game_state_data
    game_id = game_data.game_id

    new_game_state = game_dto.GameStateUpdate(
        game_id=game_id,
        new_state=game_entities.game_states.MOTION,
    )

    await update_game_state_handler.execute(new_game_state)

    await game_states_storage.add_state(
        GameStateKey(chat_id=chat_id),
        GameStateData(state=GameState.PRE_MOTION, game_id=game_id),
    )

    logger.info(
        f"{chat_id}: Состояние игры изменилось на {GameState.PRE_MOTION}"
    )

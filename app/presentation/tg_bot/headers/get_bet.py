import asyncio
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
    GameStateFilter, PlayerStateFilter
)
from app.core.game import dto as game_dto
from app.core.game import entities as game_entities
from app.presentation.tg_bot.builds.handlers import (
    update_player_bet,
    update_player_state,
    get_game_players,
    update_game_state,
    get_player,
    delete_player_by_id,
    game_over,
)
from app.presentation.tg_bot.headers.utils import start_procces_game_over


@tg_bot.message_handler(
    GameStateFilter(GameStates.BET),
    PlayerStateFilter(game_entities.player_status.BET),
)
async def _get_bet(update: Update, session: AsyncSession, bot: TgBot):
    chat_id = update.message.chat.id
    user_id = update.message.from_user.id

    update_player_bet_handler = update_player_bet(session)
    update_player_state_handler = update_player_state(session)
    player_states_storage: PlayerStatesStorage = update.player_states_storage

    bet = update.message.text  # type: ignore

    if not bet.isdigit():
        await bot.send_message(chat_id=chat_id, text="Должны быть цифры")
        return

    bet = int(bet)

    if bet >= 2**31:
        await bot.send_message(chat_id=chat_id, text="Число должно быть меньше 2**31")
        return

    player_data = player_states_storage.get_state((chat_id, user_id))
    player_id = player_data["player_id"]

    bet_dto = game_dto.Bet(player_id=player_id, bet=bet)

    await update_player_bet_handler.execute(bet_dto)

    new_state = game_dto.PlayerStateUpdate(
        player_id=player_id, new_state=game_entities.player_status.PLAYING
    )
    await update_player_state_handler.execute(new_state)
    player_states_storage.add_state(
        (chat_id, user_id),
        {
            "state": game_entities.player_status.PLAYING,
            "player_id": player_id,
        },
    )

    logger.info(f"{chat_id}: user {user_id}: сделал ставку: {bet}")
    logger.info(
        f"{chat_id}: user {user_id}: состояние сменилось на {new_state.new_state}"
    )


@tg_bot.common_handler(GameStateFilter(GameStates.PRE_BET))
async def bet_transfer_stroke(update: Update, bot: TgBot):
    if update.callback_query is not None:
        chat_id = update.callback_query.message.chat.id
        user_id = update.callback_query.from_user.id
    else:
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id

    session = await bot.get_session()
    update_player_state_handler = update_player_state(session)
    update_game_state_handler = update_game_state(session)
    get_players_handler = get_game_players(session)
    delete_player_by_id_handler = delete_player_by_id(session)
    game_over_handler = game_over(session)

    game_states_storage: GameStatesStorage = update.game_states_storage
    player_states_storage: PlayerStatesStorage = update.player_states_storage

    game_data = game_states_storage.get_state(chat_id)
    game_id = game_data["game_id"]

    game_states_storage.add_state(
        chat_id,
        {
            "state": GameStates.BET,
            "game_id": game_id,
        },
    )

    players: list[game_entities.Player] = await get_players_handler.execute(
        game_id
    )  # type: ignore

    for player in players:
        new_state = game_dto.PlayerStateUpdate(
            player_id=player.id, new_state=game_entities.player_status.BET
        )
        await update_player_state_handler.execute(new_state)
        player_states_storage.add_state(
            (chat_id, user_id),
            {"state": game_entities.player_status.BET, "player_id": player.id},
        )
        await bot.send_message(
            chat_id=chat_id, text=f"@{player.user.username} введите ставку"
        )
        await asyncio.sleep(10)

        session = await bot.get_session()
        get_player_handler = get_player(session)
        current_player = await get_player_handler.execute(player.id)
        if current_player.bet == 0:
            await bot.send_message(
                chat_id=chat_id,
                text=f"@{player.user.username} нет ставки. Удален из игры",
            )
            await delete_player_by_id_handler.execute(current_player.id)
            continue

    session = await bot.get_session()
    get_players_handler = get_game_players(session)
    players: list[game_entities.Player] = await get_players_handler.execute(
        game_id
    )  # type: ignore

    if not players:
        await bot.send_message(
            chat_id=chat_id, text="Нет участников"
        )
        await start_procces_game_over(
            update,
            bot,
            game_states_storage,
            update_game_state_handler,
            game_over_handler,
        )
        return

    text = "\n".join(
        f"{n + 1}. @{player.user.username} - {player.bet}"
        for n, player in enumerate(players)
    )
    await bot.send_message(chat_id=chat_id, text="Все ставки приняты\n" + text)

    logger.info(f"{chat_id}: Все ставки приняты")

    new_game_state = game_dto.GameStateUpdate(
        game_id=game_id,
        new_state=game_entities.game_states.MOTION,
        current_player=players[0],
    )

    await update_game_state_handler.execute(new_game_state)

    game_states_storage.add_state(
        chat_id,
        {
            "state": GameStates.PRE_MOTION,
            "game_id": game_id,
        },
    )

    logger.info(
        f"{chat_id}: Состояние игры изменилось на {new_game_state.new_state}"
    )

    print(update, '////////////////////////////')
    await bot.seng_update(update)
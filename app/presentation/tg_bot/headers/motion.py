import json
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.common.logger import logger
from app.infrastructure.tg_api import TgBot
from app.infrastructure.tg_api.dto import Update
from app.presentation.tg_bot.loader import tg_bot
from app.presentation.tg_bot.states import (
    GameStatesStorage,
    PlayerStatesStorage,
)
from app.infrastructure.tg_api.filters import GameStateFilter, PlayerStateFilter
from app.core.game import dto as game_dto
from app.core.game import entities as game_entities
from app.presentation.tg_bot.builds.handlers import (
    update_player_bet,
    update_player_state,
    get_game_players,
    update_game_state,
    get_card,
    get_player,
    game_over,
)


@tg_bot.callback_query_handler(
    GameStateFilter(game_entities.game_states.MOTION),
    PlayerStateFilter(game_entities.player_status.MOTION),
)
async def _get_card(update: Update, session: AsyncSession, bot: TgBot):
    data = update.callback_query.data  # type: ignore
    if "player_get_card" not in data:  # type: ignore
        return

    chat_id = update.callback_query.message.chat.id
    user_id = update.callback_query.from_user.id

    get_card_handler = get_card(session)
    get_player_handler = get_player(session)
    update_player_state_handler = update_player_state(session)
    player_states_storage: PlayerStatesStorage = update.player_states_storage

    player_data = player_states_storage.get_state((chat_id, user_id))
    player_id = player_data["player_id"]

    card = await get_card_handler.execute(player_id)
    player = await get_player_handler.execute(player_id)

    await bot.send_message(
        chat_id=chat_id,
        text=f"Вы вытянули карту {card.rank}.\nВаш счет: {player.score}",
    )

    if player.score > 21:
        new_state = game_dto.PlayerStateUpdate(
            player_id=player_id, new_state=game_entities.player_status.LOSE
        )
        await bot.send_message(
            chat_id=chat_id,
            text="Вы проиграли!",
        )
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

    logger.info(
        f"{chat_id}: user {user_id}: взял карту {card.rank}"
    )


@tg_bot.callback_query_handler(
    GameStateFilter(game_entities.game_states.MOTION),
    PlayerStateFilter(game_entities.player_status.MOTION),
)
async def _motion_pass(update: Update, session: AsyncSession, bot: TgBot):
    data = update.callback_query.data  # type: ignore
    if "player_pass" not in data:  # type: ignore
        return

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

    logger.info(
        f"{chat_id}: user {user_id}: пропуск хода"
    )


async def motion_transfer_stroke(
    update: Update, players: list[game_entities.Player], bot: TgBot
):
    chat_id = update.message.chat.id
    user_id = update.message.from_user.id

    session = await bot.get_session()
    update_player_state_handler = update_player_state(session)
    update_game_state_handler = update_game_state(session)
    game_over_handler = game_over(session)
    get_players_handler = get_game_players(session)

    game_states_storage: GameStatesStorage = update.game_states_storage
    player_states_storage: PlayerStatesStorage = update.player_states_storage

    game_data = game_states_storage.get_state(chat_id)
    game_id = game_data["game_id"]

    for i in range(len(players)):
        player = players[i]
        new_state = game_dto.PlayerStateUpdate(
            player_id=player.id, new_state=game_entities.player_status.MOTION
        )
        await update_player_state_handler.execute(new_state)
        player_states_storage.add_state(
            (chat_id, user_id),
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
            text=f"@{player.user.username} сделайте ход",
            reply_markup=json.dumps(inline_keyboard),
        )
        await asyncio.sleep(10)

    session = await bot.get_session()
    get_players_handler = get_game_players(session)

    players: list[game_entities.Player] = (
        await get_players_handler.execute(game_id)  # type: ignore
    )
    players = list(filter(
        lambda player: player.status == game_entities.player_status.PLAYING,
        players
    ))

    if players:
        await motion_transfer_stroke(update, players, bot)
        return

    await bot.send_message(
        chat_id=chat_id,
        text='Игра завершена\n'
    )

    logger.info(f'{chat_id}: Игра завершена')

    new_game_state = game_dto.GameStateUpdate(
        game_id=game_id,
        new_state=game_entities.game_states.STOP,
    )

    await update_game_state_handler.execute(new_game_state)
    await game_over_handler.execute(game_id)

    game_states_storage.add_state(
        chat_id,
        {
            'state': new_game_state.new_state,
            'game_id': game_id,
        }
    )

    logger.info(f"{chat_id}: Состояние игры изменилось на {new_game_state.new_state}")

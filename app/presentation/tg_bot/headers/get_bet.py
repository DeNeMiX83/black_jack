import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.common.logger import logger
from app.infrastructure.tg_api import TgBot
from app.infrastructure.tg_api.dto import Update
from app.presentation.tg_bot.loader import tg_bot
from app.presentation.tg_bot.states import (
    GameStatesStorage, PlayerStatesStorage
)
from app.infrastructure.tg_api.filters import GameStateFilter, PlayerStateFilter
from app.core.game import dto as game_dto
from app.core.game import entities as game_entities
from app.presentation.tg_bot.builds.handlers import (
    update_player_bet, update_player_state, get_game_players,
    update_game_state
)


@tg_bot.message_handler(
    GameStateFilter(game_entities.game_states.BET),
    PlayerStateFilter(game_entities.player_status.BET)
)
async def _get_bet(
    update: Update,
    session: AsyncSession,
    bot: TgBot
):
    update_player_bet_handler = update_player_bet(session)
    update_player_state_handler = update_player_state(session)
    player_states_storage: PlayerStatesStorage = update.player_states_storage

    bet = update.message.text  # type: ignore

    if not bet.isdigit():
        await bot.send_message(
            chat_id=update.message.chat.id,
            text='Неверный формат ставки'
        )
        return
    bet = int(bet)

    player_data = player_states_storage.get_state(
        (update.message.chat.id, update.message.from_user.id)
    )

    bet_dto = game_dto.Bet(
        player_id=player_data['player_id'],
        bet=bet
    )

    await update_player_bet_handler.execute(bet_dto)

    new_state = game_dto.PlayerStateUpdate(
        player_id=player_data['player_id'],
        new_state=game_entities.player_status.PLAYING
    )
    await update_player_state_handler.execute(new_state)
    player_states_storage.add_state(
        (update.message.chat.id, player_data['player_id']),
        {
            'state': game_entities.player_status.PLAYING
        }
    )

    logger.info(f'{update.message.chat.id}: сделал ставку: {bet}')


async def transfer_stroke(
    update: Update,
    players: list[game_entities.Player],
    bot: TgBot
):
    chat_id = update.message.chat.id
    user_id = update.message.from_user.id

    session = await bot.get_session()
    update_player_state_handler = update_player_state(session)
    update_game_state_handler = update_game_state(session)
    get_players_handler = get_game_players(session)

    game_states_storage: GameStatesStorage = update.game_states_storage
    player_states_storage: PlayerStatesStorage = update.player_states_storage

    game_data = game_states_storage.get_state(chat_id)
    game_id = game_data['game_id']

    for player in players:
        new_state = game_dto.PlayerStateUpdate(
            player_id=player.id,
            new_state=game_entities.player_status.BET
        )
        await update_player_state_handler.execute(new_state)
        player_states_storage.add_state(
            (chat_id, user_id),
            {
                'state': game_entities.player_status.BET,
                'player_id': player.id
            }
        )
        await bot.send_message(
            chat_id=chat_id,
            text=f'@{player.user.username} введите ставку'
        )
        await asyncio.sleep(10)

    players: list[game_entities.Player] = (
        await get_players_handler.execute(game_id)  # type: ignore
    )

    text = '\n'.join(
        f'{n + 1}. @{player.user.username} - {player.bet}'
        for n, player in enumerate(players)
    )
    await bot.send_message(
        chat_id=chat_id,
        text='Все ставки приняты\n' + text
    )

    logger.info(f'{chat_id}: Все ставки приняты')

    new_game_state = game_dto.GameStateUpdate(
        game_id=game_id,
        new_state=game_entities.game_states.MOTION,
        current_player=players[0]
    )

    await update_game_state_handler.execute(new_game_state)

    game_states_storage.add_state(
        chat_id,
        {
            'state': new_game_state.new_state,
            'game_id': game_id,
        }
    )


    logger.info(f"{chat_id}: Состояние игры изменилось на {new_game_state.new_state}")


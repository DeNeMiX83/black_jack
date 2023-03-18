import logging
from app.core.game import dto as game_dto
from app.core.game import entities as game_entities
from app.infrastructure.tg_api import TgBot
from app.infrastructure.tg_api.dto import Update
from app.presentation.tg_bot.builders import (
    update_game_state,
    game_over,
)
from app.infrastructure.tg_api.states import (
    GameState,
    GameStateKey,
    GameStateData
)

logger = logging.getLogger()


async def start_procces_game_over(
    update: Update,
    bot: TgBot,
):
    chat_id = update.message.chat.id

    session = await bot.get_session()
    game_states_storage = await bot.get_game_states_storage()
    update_game_state_handler = update_game_state(session)
    game_over_handler = game_over(session)

    game_data = update.game_state_data
    game_id = game_data.game_id

    await bot.send_message(
        chat_id=update.message.chat.id, text="Игра завершена"
    )
    new_game_state = game_dto.GameStateUpdate(
        game_id=game_id,
        new_state=game_entities.game_states.STOP,
    )

    await update_game_state_handler.execute(new_game_state)
    await game_over_handler.execute(game_id)

    await game_states_storage.add_state(
        GameStateKey(chat_id=chat_id),
        GameStateData(state=GameState.MOTION, game_id=game_id),
    )

    logger.info(f"{chat_id}: Состояние игры изменилось " +
                f"на {new_game_state.new_state}")
    logger.info(f"{chat_id}: Игра завершена")

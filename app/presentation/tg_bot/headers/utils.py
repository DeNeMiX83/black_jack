from app.common.logger import logger
from app.core.game import dto as game_dto
from app.core.game import entities as game_entities
from app.infrastructure.tg_api import TgBot
from app.infrastructure.tg_api.dto import Update
from app.presentation.tg_bot.states import GameStatesStorage
from app.core.game.handlers import (
    UpdateGameStateHandler,
    GameOverHandler
)


async def start_procces_game_over(
    update: Update,
    bot: TgBot,
    game_states_storage: GameStatesStorage,
    update_game_state_handler: UpdateGameStateHandler,
    game_over_handler: GameOverHandler,
):
    chat_id = update.message.chat.id

    game_data = game_states_storage.get_state(chat_id)
    game_id = game_data["game_id"]

    await bot.send_message(
        chat_id=update.message.chat.id, text="Игра завершена"
    )
    new_game_state = game_dto.GameStateUpdate(
        game_id=game_id,
        new_state=game_entities.game_states.STOP,
    )

    await update_game_state_handler.execute(new_game_state)
    await game_over_handler.execute(game_id)

    game_states_storage.add_state(
        chat_id,
        {
            "state": new_game_state.new_state,
            "game_id": game_id,
        },
    )

    logger.info(f"{chat_id}: Игра завершена")
    return

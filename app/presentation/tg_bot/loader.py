from app.di.container import Container
from app.infrastructure.tg_api import TgBot
from app.presentation.tg_bot.states import (
    GameStatesStorage, PlayerStatesStorage
)
from app.presentation.tg_bot import build_di


container = Container()
tg_bot = TgBot(container)
game_states_storage = GameStatesStorage()
player_states_storage = PlayerStatesStorage()
container.register(TgBot, tg_bot)
container.register(GameStatesStorage, game_states_storage)
container.register(PlayerStatesStorage, player_states_storage)
build_di.build(container)

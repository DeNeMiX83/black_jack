from app.di.container import Container
from app.infrastructure.tg_api import TgBot
from app.presentation.tg_bot import build_di


container = Container()
tg_bot = TgBot(container)
container.register(TgBot, tg_bot)
# from pprint import pprint
# pprint(container.dependencies)
build_di.build(container)

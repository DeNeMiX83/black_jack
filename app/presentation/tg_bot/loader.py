import logging.config
from app.di.container import Container
from app.config.settings import Settings
from app.infrastructure.tg_api import TgBot

from app.presentation.tg_bot.builders import build_di


settings = Settings()
container = Container()
tg_bot = TgBot(settings, container)

container.register(Settings, settings)
container.register(TgBot, tg_bot)

build_di.build(container)

logging.config.fileConfig(settings.logging_config_path)
logger = logging.getLogger()
logger.info("Starting")
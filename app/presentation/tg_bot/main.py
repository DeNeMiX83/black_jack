import asyncio
from app.infrastructure.store.sqlalchemy.models.mapping import start_mappers
from app.infrastructure.tg_api.bot import TgBot
from app.core.game.entities import Game
from sqlalchemy import update


async def main():
    from .loader import container  # noqa
    from app.presentation.tg_bot.handlers import tg_bot  # noqa

    start_mappers()
    await finish_all_games_started(tg_bot)
    await tg_bot.start()


async def finish_all_games_started(tg_bot: TgBot):
    session = await tg_bot.get_session()
    stmt = update(Game).where(Game.is_over==False).values(is_over=True)
    await session.execute(stmt)
    try:
        await session.commit()
    except Exception:
        pass


if __name__ == "__main__":
    asyncio.run(main())

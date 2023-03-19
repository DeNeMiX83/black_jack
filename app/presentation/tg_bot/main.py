import asyncio
from app.infrastructure.store.sqlalchemy.models.mapping import start_mappers
from app.infrastructure.tg_api.bot import TgBot
from app.core.game.entities import Game
from sqlalchemy import update
from .middlewares import ThrottlingMiddleware


async def main():
    from .loader import container  # noqa
    from app.presentation.tg_bot.handlers import tg_bot  # noqa

    start_mappers()
    await finish_not_over_games(tg_bot)
    throttling_middleware = ThrottlingMiddleware(tg_bot)
    tg_bot.add_middleware(throttling_middleware)
    await tg_bot.start()


async def finish_not_over_games(tg_bot: TgBot):
    session = await tg_bot.get_session()
    stmt = update(Game).where(Game.is_over == False).values(is_over=True)  # type: ignore # noqa
    await session.execute(stmt)
    try:
        await session.commit()
    except Exception:
        pass


if __name__ == "__main__":
    asyncio.run(main())

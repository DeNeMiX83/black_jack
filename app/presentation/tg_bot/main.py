import asyncio
from app.infrastructure.store.sqlalchemy.models.mapping import start_mappers


async def main():
    from .loader import container # noqa
    from app.presentation.tg_bot.headers import tg_bot # noqa

    start_mappers()
    await tg_bot.start()


if __name__ == '__main__':
    asyncio.run(main())

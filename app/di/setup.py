from app.di import Container


async def setup_container() -> Container:
    container = Container()
    return container

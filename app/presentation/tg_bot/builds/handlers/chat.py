from sqlalchemy.ext.asyncio import AsyncSession
from app.di.container import Container
from app.infrastructure.store.sqlalchemy.gateway import (
    ChatGatewayImpl, CommiterImp
)
from app.core.chat.handlers import CreateChatHandler


def build(container: Container) -> None:
    container.register(CreateChatHandler, chat_create)


def chat_create(
    session: AsyncSession,
) -> CreateChatHandler:
    chat_gateway = ChatGatewayImpl(session)
    commiter = CommiterImp(session)
    return CreateChatHandler(chat_gateway, commiter)

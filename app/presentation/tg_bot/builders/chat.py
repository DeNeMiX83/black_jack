from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.store.sqlalchemy.gateway import (
    ChatGatewayImpl,
    CommiterImp,
)
from app.core.chat.handlers import CreateChatHandler


def chat_create(
    session: AsyncSession,
) -> CreateChatHandler:
    chat_gateway = ChatGatewayImpl(session)
    commiter = CommiterImp(session)
    return CreateChatHandler(chat_gateway, commiter)

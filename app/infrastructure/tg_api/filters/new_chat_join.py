from app.infrastructure.tg_api.filters import Filter
from app.infrastructure.tg_api.dto import Update


class NewChatJoinFilter(Filter):
    def check(self, update: Update):
        return (
            update.message
            and update.message.new_chat_member is not None
        )

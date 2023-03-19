from app.infrastructure.tg_api.filters import Filter
from app.infrastructure.tg_api.dto import Update


class MessageFilter(Filter):
    def check(self, update: Update) -> bool:
        return update.message is not None and update.message.text is not None


class CallbackQueryFilter(Filter):
    def check(self, update: Update):
        return update.callback_query is not None


class CallbackQueryDataFilter(Filter):
    def __init__(self, callback_data: str):
        self._callback_data = callback_data

    def check(self, update: Update):
        return (
            update.callback_query is not None
            and update.callback_query.data == self._callback_data
        )


class GroupFilter(Filter):
    def check(self, update: Update) -> bool:
        return update.message.chat.type == "group"  # type: ignore


class CommandFilter(Filter):
    def __init__(self, command: str) -> None:
        self._command = command

    def check(self, update: Update):
        if (entities := update.message.entities) is not None:  # type: ignore # noqa
            if entities[-1].type == "bot_command":
                offset = entities[-1].offset
                length = entities[-1].length
                if (
                    self._command in update.message.text[offset : offset + length + 1]  # type: ignore # noqa
                ):
                    return True
        return False

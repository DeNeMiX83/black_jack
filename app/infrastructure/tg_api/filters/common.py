from app.infrastructure.tg_api.filters import Filter
from app.infrastructure.tg_api.dto import Update


class MessageFilter(Filter):
    def check(self, update: Update) -> bool:
        return update.message is not None and update.message.text is not None


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
                    update.message.text[offset:offset + length + 1]  # type: ignore # noqa
                    == self._command
                ):
                    return True
        return False

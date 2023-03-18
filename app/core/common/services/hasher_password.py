from passlib.context import CryptContext
from app.core.common.protocols import HasherPasswordService
from app.config.settings import Settings


class HasherPasswordServiceImp(HasherPasswordService):
    def __init__(self, settings: Settings):
        self._pwd_context = CryptContext(
            schemes=[settings.password_algorithm],
            deprecated="auto"
        )

    def hash(self, password: str) -> str:
        return self._pwd_context.hash(password)

    def verify_password(self, raw_password: str, hashed_password: str) -> bool:
        return self._pwd_context.verify(raw_password, hashed_password)

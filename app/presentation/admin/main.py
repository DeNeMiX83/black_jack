from aiohttp_session import setup as session_setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from app.presentation.admin.common import Application

app = Application()


def setup_app(config_path: str) -> Application:
    session_setup(app, EncryptedCookieStorage(app.settings.secret_key))
    return app

import os
from dataclasses import dataclass, field


@dataclass
class Settings:
    secret_key: str = field(init=False)
    password_algorithm: str = field(init=False)
    tg_api_url: str = field(init=False)
    tg_api_url_with_token: str = field(init=False)
    tg_bot_token: str = field(init=False)
    postgres: "PostgresSettings" = field(init=False)

    def __post_init__(self):
        self.secret_key = os.getenv("SECRET_KEY")
        self.password_algorithm = os.getenv("PASSWORD_ALGORITHM")
        self.tg_api_url = os.getenv("TG_API_URL")
        self.tg_bot_token = os.getenv("TG_BOT_TOKEN")
        self.tg_api_url_with_token = (
            f'{self.tg_api_url}/bot{self.tg_bot_token}'
        )
        self.postgres = PostgresSettings()


@dataclass
class PostgresSettings:
    host: str = field(init=False)
    port: int = field(init=False)
    user: str = field(init=False)
    password: str = field(init=False)
    database: str = field(init=False)
    url: str = field(init=False)

    def __post_init__(self):
        self.host = os.getenv("POSTGRES_HOST")
        self.port = os.getenv("POSTGRES_PORT")
        self.user = os.getenv("POSTGRES_USER")
        self.password = os.getenv("POSTGRES_PASSWORD")
        self.database = os.getenv("POSTGRES_DB")
        self.url = (
            "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}".format(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database,
            )
        )

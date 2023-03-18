import os
from dataclasses import dataclass, field


@dataclass
class AdminApiSettings:
    host: str = field(init=False)
    port: int = field(init=False)
    admin_email: str = field(init=False)
    admin_password: str = field(init=False)

    def __post_init__(self):
        self.host = os.getenv("ADMIN_API_HOST")
        self.port = os.getenv("ADMIN_API_PORT")
        self.admin_email = os.getenv("ADMIN_API_ADMIN_EMAIL")
        self.admin_password = os.getenv("ADMIN_API_ADMIN_PASSWORD")


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
        self.url = "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}".format(
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
        )


@dataclass
class RedisSettings:
    host: str = field(init=False)
    port: int = field(init=False)
    db: int = field(init=False)

    def __post_init__(self):
        self.host = os.getenv("REDIS_HOST")
        self.port = os.getenv("REDIS_PORT")
        self.db = os.getenv("REDIS_DB")


@dataclass
class RabbitMQSettings:
    username: str = field(init=False)
    password: str = field(init=False)
    host: str = field(init=False)
    port: int = field(init=False)
    queue: str = field(init=False)
    url: str = field(init=False)

    def __post_init__(self):
        self.username = os.getenv("RABBIT_USERNAME")
        self.password = os.getenv("RABBIT_PASSWORD")
        self.host = os.getenv("RABBIT_HOST")
        self.port = os.getenv("RABBIT_PORT")
        self.queue = os.getenv("RABBIT_QUEUE")
        self.url = "amqp://{username}:{password}@{host}:{port}/".format(
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
        )


@dataclass
class Settings:
    secret_key: str = field(init=False)
    session_key: str = field(init=False)
    password_algorithm: str = field(init=False)
    logging_config_path: str = field(init=False)

    tg_api_url: str = field(init=False)
    tg_api_url_with_token: str = field(init=False)
    tg_bot_token: str = field(init=False)

    admin_api: AdminApiSettings = field(
        init=False, default_factory=AdminApiSettings
    )
    postgres: PostgresSettings = field(
        init=False, default_factory=PostgresSettings
    )
    redis: RedisSettings = field(init=False, default_factory=RedisSettings)
    rabbitmq: RabbitMQSettings = field(
        init=False, default_factory=RabbitMQSettings
    )

    def __post_init__(self):
        self.secret_key = os.getenv("SECRET_KEY")
        self.session_key = os.getenv("SESSION_KEY")
        self.password_algorithm = os.getenv("PASSWORD_ALGORITHM")
        self.logging_config_path = os.getenv("LOGGING_CONFIG_PATH")

        self.tg_api_url = os.getenv("TG_API_URL")
        self.tg_bot_token = os.getenv("TG_BOT_TOKEN")
        self.tg_api_url_with_token = f"{self.tg_api_url}/bot{self.tg_bot_token}"

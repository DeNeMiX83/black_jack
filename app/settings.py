import os
from dataclasses import dataclass, field


@dataclass
class Settings:
    secret_key: str = field(init=False)
    password_algorithm = field(init=False)
    postgres: "PostgresSettings" = field(init=False)

    def __post_init__(self):
        self.password_algorithm = os.getenv("PASSWORD_ALGORITHM")
        self.postgtess = PostgresSettings()


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
            "postgresql://{user}:{password}@{host}:{port}/{database}".format(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database,
            )
        )

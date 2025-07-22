"""..."""

from datetime import timedelta
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    """..."""

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent.parent / ".env", extra="ignore"
    )


class PostgresConfig(BaseConfig):
    """..."""

    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def url(self) -> str:
        """..."""
        return f"postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class SQLiteConfig(BaseConfig):
    """..."""

    SQLITE_DB_PATH: str

    @property
    def url(self) -> str:
        """..."""
        return f"sqlite:///{self.SQLITE_DB_PATH}"


class JWTConfig(BaseConfig):
    """..."""

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    @property
    def access_token_expires(self) -> timedelta:
        return timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)


class Settings(BaseSettings):
    """..."""

    postgres: PostgresConfig = PostgresConfig()
    sqlite: SQLiteConfig = SQLiteConfig()
    jwt: JWTConfig = JWTConfig()


settings = Settings()

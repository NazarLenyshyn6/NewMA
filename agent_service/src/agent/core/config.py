"""..."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    """..."""

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent.parent.parent / ".env",
        extra="ignore",
    )


class AnthropicModelConfig(BaseConfig):
    """..."""

    ANTHROPIC_API_KEY: str


class Settings(BaseSettings):
    """..."""

    anthropic_model: AnthropicModelConfig = AnthropicModelConfig()


settings = Settings()

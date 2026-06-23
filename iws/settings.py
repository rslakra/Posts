#
# Author: Rohtash Lakra
#
from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigSetting(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow",
    )

#
# Author: Rohtash Lakra
#
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

from framework.enums.env_type import EnvType


def envFileName() -> str:
    """Returns the name of the env file to load: '.env.test' for the testing env otherwise '.env'.

    The testing env is selected with the ENV_TYPE environment variable (e.g. tests/__init__.py sets ENV_TYPE=test), so
    that the tests never use the settings (e.g. the database) of the development environment.
    """
    return ".env.test" if EnvType.is_testing(EnvType.get_env_type()) else ".env"


ENV_FILE = envFileName()


class ConfigSetting(BaseSettings):
    """Application settings loaded from environment variables (which take precedence) and the env file."""

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow",
    )

    # Database settings are declared explicitly so that real environment variables (e.g. 'docker run -e DB_TYPE=MYSQL')
    # override the values of the env file. Undeclared keys of the env file are still kept via extra="allow".
    DB_TYPE: Optional[str] = None
    DB_NAME: Optional[str] = None
    DB_PATH: Optional[str] = None
    DB_HOSTNAME: Optional[str] = None
    DB_PORT: Optional[str] = None
    DB_USERNAME: Optional[str] = None
    DB_PASSWORD: Optional[str] = None

import os
from enum import unique

from framework.enums.base import BaseEnum, KeyEnum


@unique
class EnvType(BaseEnum):
    """EnvType class represents various supported env types"""
    # The environment where developers write and test code
    DEV = ("development", "develop", "dev")
    LOCAL = ("local", "localhost")
    PROD = ("production", "live", "prod")
    # A testing environment
    QA = ("qa")
    # A testing environment
    STAGE = ("staging", "stage")
    # A testing environment
    TEST = ("testing", "test")
    #  UAT or “User Acceptance Testing” Environment - testing environment
    UAT = ("uat")

    @staticmethod
    def is_development(env_type: str) -> bool:
        """Returns true if DEV == env_type other false"""
        return EnvType.equals(EnvType.DEV, env_type)

    @staticmethod
    def is_local(env_type: str) -> bool:
        """Returns true if LOCAL == env_type other false"""
        return EnvType.equals(EnvType.LOCAL, env_type)

    @staticmethod
    def is_production(env_type: str) -> bool:
        """Returns true if PROD == env_type other false"""
        return EnvType.equals(EnvType.PROD, env_type)

    @staticmethod
    def is_qa(env_type: str) -> bool:
        """Returns true if QA == env_type other false"""
        print(f"is_qa => env_type={env_type}")
        return EnvType.equals(EnvType.QA, env_type)

    @staticmethod
    def is_staging(env_type: str) -> bool:
        """Returns true if STAGE == env_type other false"""
        return EnvType.equals(EnvType.STAGE, env_type)

    @staticmethod
    def is_testing(env_type: str) -> bool:
        """Returns true if TEST == env_type other false"""
        return EnvType.equals(EnvType.TEST, env_type)

    @staticmethod
    def is_uat(env_type: str) -> bool:
        """Returns true if UAT == env_type other false"""
        return EnvType.equals(EnvType.UAT, env_type)

    @classmethod
    def get_env_type(cls):
        env_type = os.getenv(KeyEnum.ENV_TYPE.name)
        if env_type is None:
            env_type = os.getenv(KeyEnum.ENV_TYPE.name.lower())
            if env_type is None:
                env_type = EnvType.flask_env()
                if env_type is None:
                    env_type = EnvType.DEV.name

        return env_type

    @staticmethod
    def flask_env() -> str:
        """Returns the value of FLASK_ENV env variable value if set otherwise None."""
        flask_env = os.getenv(KeyEnum.FLASK_ENV.name)
        if flask_env is None:
            flask_env = os.getenv(KeyEnum.FLASK_ENV.name.lower())

        return flask_env

    @classmethod
    def getenv_bool(cls, key: str, default=False):
        """Get an environment variable boolean value, return False if it doesn't exist.
        The optional second argument can specify an alternate default.
        key, default and the result are bool."""
        return os.getenv(key, str(default)).lower() in ("yes", "true", "1")


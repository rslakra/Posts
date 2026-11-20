import os
from enum import unique
from typing import Any
from urllib.parse import quote_plus

from framework.enums.base import BaseEnum, KeyEnum


@unique
class DbType(BaseEnum):
    """Database Type Enum. For readability, add constants in Alphabetical order."""
    SQLALCHEMY = "sqlite:///"
    # The connector uses synchronous SQLAlchemy engines/sessions, so a synchronous driver (PyMySQL) is required.
    MYSQL = "mysql+pymysql://"

    @classmethod
    def dbUri(cls, configs: dict[str, Any] = None) -> str:
        """Returns DB URI string"""
        dbType = configs.get(KeyEnum.DB_TYPE.name)
        if dbType and DbType.SQLALCHEMY == DbType.of_name(dbType):
            # For SQLite, allow explicit DB_PATH override from .env.
            # If DB_PATH is not provided, fallback to DB_NAME behavior.
            dbName = configs.get("DB_NAME")
            dbPath = configs.get("DB_PATH")
            if dbPath:
                # Expand user/environment values (e.g. "~/Downloads/...").
                resolvedPath = os.path.expandvars(os.path.expanduser(str(dbPath).strip()))
                # Treat paths with .db suffix as explicit file paths; otherwise as directories.
                if resolvedPath.lower().endswith(".db"):
                    sqliteFilePath = resolvedPath
                else:
                    sqliteFileName = dbName if str(dbName).lower().endswith(".db") else f"{dbName}.db"
                    sqliteFilePath = os.path.join(resolvedPath, sqliteFileName)

                return f"sqlite:////{sqliteFilePath.lstrip('/')}"

            return ''.join([DbType.SQLALCHEMY.value, dbName])
        elif dbType and DbType.MYSQL == DbType.of_name(dbType):
            # db_uri = f"mysql+pymysql://{username}:{password}@{hostname}:{port}/{db_name}"
            # DB_HOSTNAME is the documented key (.env), DB_HOST is accepted as an alias.
            dbHost = configs.get("DB_HOSTNAME") or configs.get("DB_HOST") or "127.0.0.1"
            dbPort = configs.get("DB_PORT") or 3306
            dbUserName = quote_plus(str(configs.get("DB_USERNAME") or ""))
            dbPassword = quote_plus(str(configs.get("DB_PASSWORD") or ""))
            dbName = configs.get("DB_NAME")
            return f"{DbType.MYSQL.value}{dbUserName}:{dbPassword}@{dbHost}:{dbPort}/{dbName}"
        else:
            raise ValueError(f"Unsupported dbType={dbType}!")

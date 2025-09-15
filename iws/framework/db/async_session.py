#
# Author: Rohtash Lakra
#
import logging
import os
from asyncio import current_task
from collections.abc import AsyncIterator
from pathlib import Path
from typing import Any

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
    AsyncSession,
)

from framework.enums import DbType
from framework.enums import EnvType

logger = logging.getLogger(__name__)


class AsyncSessionManager:
    """Creates an AsyncSession and managing its lifecycle using the asyncio module, along with demonstrating the use
    of dependency injection for cleaner and more maintainable code.
    """

    def __init__(self, engine=None, metadata=None):
        """Initialize Async Session Manager"""
        logger.debug(f"AsyncSessionManager({engine}, {metadata})")
        logger.debug("Initializing Async Session Manager ...")
        self._configInitialized = False
        self.app = None
        self.db_name: str = None
        self.db_user_name = None
        self.db_password = None

        self.pool = None
        self.db_uri = None
        self.engine: AsyncEngine | None = None
        self.metadata = metadata
        self.session_maker = None
        self.session = None

        # paths
        self.cur_dir = Path(__file__).parent
        # logger.debug(f"cur_dir:{self.cur_dir}")
        self.data_path = self.cur_dir.joinpath("data")
        # logger.debug(f"data_path:{self.data_path}")

    @property
    def isConfigInitialized(self):
        return self._configInitialized

    def _init_configs(self, configs: dict[str, Any] = None):
        """Initializes Connector's Configs"""
        logger.debug(f"Initializing Connector's Configs ...")
        if not self.isConfigInitialized:
            self.dbUrl = os.getenv("DATABASE_URL")
            self.defaultPoolSize = int(os.getenv("DEFAULT_POOL_SIZE", 1))
            self.poolSize = int(os.getenv("RDS_POOL_SIZE", 1))
            self.autoCommit = EnvType.getenv_bool(os.getenv("AUTO_COMMIT", False))
            self.poolSize += self.defaultPoolSize
            # validate the pool size
            if (self.poolSize - self.defaultPoolSize) < 1:
                raise Exception('poolSize should be higher that 0!')

            # logger.debug(f"current_app: {current_app}, current_app.config: {current_app.config}")
            # read db-name from app's config
            if not self.db_name:
                self.db_name = configs.get("DB_NAME")

            logger.debug(f"self.db_name={self.db_name}")
            if self.db_name and not self.db_name.endswith(".db"):
                self.db_name = '.'.join([self.db_name, "db"])
                configs["DB_NAME"] = self.db_name

            # build db uri
            self.db_uri = DbType.dbUri(configs)
            self.db_password = configs.get("DB_PASSWORD")
            logger.debug(f"db_name={self.db_name}, db_password={self.db_password}, db_uri={self.db_uri}")
            self._configInitialized = True
        else:
            logger.debug("Connector's Configs already Initialized.")

    def init_db(self, app: None, configs: dict[str, Any] = None) -> None:
        """Initializes the database"""
        logger.debug(f"Initializing Database. configs={configs}")
        self.app = app
        self._init_configs(configs)
        # Creating an asynchronous engine
        self.engine = create_async_engine(
            self.dbUrl,
            pool_size=self.poolSize,
            max_overflow=0,
            pool_pre_ping=False,
            echo=True
        )

        # Creating an asynchronous session class
        self.session_maker = async_sessionmaker(
            autocommit=self.autoCommit, autoflush=False, bind=self.engine
        )

        # Creating a scoped session
        self.session = async_scoped_session(self.session_maker, scopefunc=current_task)

    async def close(self):
        """Closing the database session."""

        if self.engine is None:
            raise Exception("AsyncSessionManager is not initialized!")

        await self.engine.dispose()

    async def getSession(self) -> AsyncIterator[AsyncSession]:
        """Initialize and close the database session properly. It ensures that we have a valid and scoped database
        session for each request.
        """

        session = self.session()
        if session is None:
            raise Exception("AsyncSessionManager is not initialized!")

        try:
            # Setting the search path and yielding the session...
            # TODO: FIX ME
            # await session.execute(
            #     text(f"SET search_path TO {SCHEMA}")
            # )
            yield session

        except Exception:
            await session.rollback()
            raise

        finally:
            # Closing the session after use...
            await session.close()


# Note: - move to middleware
# Initialize the DatabaseSessionManager
sessionManager = AsyncSessionManager()

#
# Author: Rohtash Lakra
#
import logging
import sqlite3
from contextvars import ContextVar
from pathlib import Path
from typing import Iterator
from typing import Union, Iterable, Any

import sqlalchemy
from sqlalchemy import Engine, URL, create_engine
from sqlalchemy.orm import Session, sessionmaker

from framework.enums.base import KeyEnum
from framework.enums.db_type import DbType
from framework.orm.sqlalchemy.schema import BaseSchema

logger = logging.getLogger(__name__)


@staticmethod
def createEngine(dbUri: Union[str, URL], debug: bool = False) -> Engine:
    """Create a new :class:`Engine` instance.

    The debug=True parameter indicates that SQL emitted by connections will be logged to standard out.
    """
    logger.debug(f"+createEngine({dbUri}, {debug})")
    # Ensure SQLite parent directory exists for explicit DB_PATH file locations.
    if isinstance(dbUri, str) and dbUri.startswith("sqlite:////"):
        sqlite_file_path = "/" + dbUri.removeprefix("sqlite:////")
        Path(sqlite_file_path).parent.mkdir(parents=True, exist_ok=True)
    engine = create_engine(dbUri, pool_recycle=3600, echo=debug)
    engine.execution_options(isolation_level="AUTOCOMMIT")
    logger.debug(f"-createEngine(), engine={engine}")
    return engine


@staticmethod
def createSessionMaker(engine: Engine):
    """Create a new :class:`Engine` instance."""
    logger.debug(f"+createSessionMaker({engine})")
    sessionMaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.debug(f"-createSessionMaker(), sessionMaker={sessionMaker}")
    return sessionMaker


@staticmethod
def createDatabase(engine: Engine) -> None:
    """ Creates the database. """
    logger.debug(f"+createDatabase({engine})")
    # Using our table metadata and our engine, we can generate our schema at once in our target
    # database, using a method called 'MetaData.create_all()':
    try:
        BaseSchema.metadata.create_all(bind=engine)
    except Exception as ex:
        logger.error(f"Error while creating database! Exception={ex}")

    logger.debug(f"-createDatabase(), engine={engine}")


# Define Constants
KEY_CONNECTION = 'connection'
KEY_POOL_NAME = 'sqlite3_pool'
SQLITE_PREFIX = 'sqlite:///'


class DatabaseConnector(object):
    """Database Connector"""

    def __init__(self):
        logger.debug("Initializing Connector ...")
        self.UTF_8 = 'UTF-8'

    def init(self, app=None):
        logger.debug("Initializing Connector with application ...")

    def init_db(self, configs: dict = None):
        logger.debug("Initializing database ...")


class AsyncSQLite3Connector(DatabaseConnector):
    """Database connector used by the FastAPI application.

    It builds a SQLAlchemy engine (SQLite by default, MySQL when DB_TYPE=MYSQL) from the application's settings
    and provides sessions to the repositories and the route dependencies.
    """

    def __init__(self):
        """Initialize"""
        logger.debug("Initializing Async SQLite3 Connector ...")
        self.context: ContextVar[Any] = ContextVar('connection', default=None)
        self._configInitialized = False
        self.app = None
        self.pool = None
        self.db_name: str = None
        self.db_user_name = None
        self.db_password = None
        self.db_uri = None
        self.engine: Engine = None
        self.sessionMaker = None
        # Database table definitions.
        self.metadata = sqlalchemy.MetaData()

        # paths
        self.cur_dir = Path(__file__).parent
        self.data_path = self.cur_dir.joinpath("data")

    @property
    def isConfigInitialized(self):
        return self._configInitialized

    @staticmethod
    def _isSQLite(configs: dict[str, Any]) -> bool:
        dbType = configs.get(KeyEnum.DB_TYPE.name)
        return bool(dbType) and DbType.equals(DbType.SQLALCHEMY, dbType)

    def _init_configs(self, configs: dict[str, Any] = None):
        """Initializes Connector's Configs"""
        logger.debug(f"Initializing Connector's Configs ...")
        if not self.isConfigInitialized:
            # read db-name from the configs
            if not self.db_name:
                self.db_name = configs.get("DB_NAME")

            logger.debug(f"self.db_name={self.db_name}")
            # only SQLite databases are files that carry the '.db' extension.
            if self._isSQLite(configs) and self.db_name and not self.db_name.endswith(".db"):
                self.db_name = '.'.join([self.db_name, "db"])
                configs["DB_NAME"] = self.db_name

            # build db uri
            self.db_uri = DbType.dbUri(configs)
            self.db_password = configs.get("DB_PASSWORD")
            # never log the uri, it may contain credentials.
            logger.debug(f"db_name={self.db_name}")
            self._configInitialized = True
        else:
            logger.debug("Connector's Configs already Initialized.")

    def init_db(self, app: None, configs: dict[str, Any] = None) -> None:
        """Initializes the database"""
        logger.debug(f"Initializing Database.")
        self.app = app
        self._init_configs(configs)

        dbType = configs.get(KeyEnum.DB_TYPE.name)
        logger.debug(f"dbType={dbType}")
        if dbType and (DbType.equals(DbType.SQLALCHEMY, dbType) or DbType.equals(DbType.MYSQL, dbType)):
            # SQLAlchemy DB Creation
            self.engine = createEngine(self.db_uri, debug=True)
            self.sessionMaker = createSessionMaker(self.engine)
            createDatabase(self.engine)

    def getConnection(self):
        """Returns SQLite3 Connection"""
        logger.debug(f"getConnection(), db_name: {self.db_name}")
        return sqlite3.connect(self.db_name, detect_types=sqlite3.PARSE_DECLTYPES)

    def openConnection(self):
        """Opens the database connection"""
        logger.debug("Opening database connection ...")
        connection = self.context.get()
        if connection is None:
            connection = self.getConnection()
            connection.row_factory = sqlite3.Row
            self.context.set(connection)
            logger.debug(f"connection: {connection}")

        return connection

    def closeConnection(self, connection=None, error=None):
        """Closes the database connection"""
        logger.debug(f"Closing Database Connection. connection={connection}, error={error}")
        connection = connection or self.context.get()
        if connection:
            try:
                try:
                    if error:
                        connection.rollback()
                        logger.warning('Rollback occurred due to an error!')
                except Exception as ex:
                    logger.warning(f'Error while rollback/closing the cursor! Error:{ex}')
                finally:
                    connection.close()
                    self.context.set(None)
            except Exception as ex:
                logger.warning(f'Error while closing the connection! Error:{ex}')
        else:
            logger.debug('No active connection!')

    def getSession(self) -> Iterator[Session]:
        """
        Provides a managed session, usable as a FastAPI dependency (`Depends(connector.getSession)`).

        Yields:
            Session: A new database session that commits on success and rolls back on error.
        """
        if self.sessionMaker is None:
            raise Exception("AsyncSQLite3Connector is not initialized!")

        session = self.sessionMaker()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def save(self, instance):
        """Saves the instance using context manager"""
        logger.debug(f"+save(), instance={instance}")
        with Session(self.engine) as session:
            try:
                session.begin()
                session.add(instance)
            except Exception as ex:
                logger.error(f"Failed transaction with error:{ex}")
                session.rollback()
                raise ex
            else:
                session.commit()
                logger.debug("Persisted a instance successfully!")
        logger.debug(f"-save()")

    def save_all(self, instances: Iterable[object]):
        """Saves the instances using context manager"""
        logger.debug(f"+save_all(), instances={instances}")
        with Session(self.engine) as session:
            try:
                session.begin()
                session.add_all(instances)
            except Exception as ex:
                logger.error(f"Failed transaction with error:{ex}")
                session.rollback()
                raise ex
            else:
                session.commit()
                logger.debug(f"Persisted [{len(instances)}] instances successfully!")
        logger.debug("-save_all()")

    def select(self, entity: BaseSchema):
        """Selects the first instance"""
        logger.debug(f"select => entity={entity}")
        with Session(self.engine) as session:
            return session.query(entity).first()

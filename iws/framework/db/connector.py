#
# Author: Rohtash Lakra
#
import logging
import sqlite3
from pathlib import Path
from typing import Union, Iterable

import click
from flask import Flask, g, current_app
from sqlalchemy import Engine, URL, create_engine
from sqlalchemy.orm import Session

from framework.enums import KeyEnum
from framework.orm.sqlalchemy.schema import BaseSchema

logger = logging.getLogger(__name__)


@staticmethod
def createEngine(dbUri: Union[str, URL], debug: bool = False) -> Engine:
    """Create a new :class:`Engine` instance.

    The debug=True parameter indicates that SQL emitted by connections will be logged to standard out.
    """
    logger.debug(f"+createEngine({dbUri}, {debug})")
    engine = create_engine(dbUri, pool_recycle=3600, echo=debug)
    engine.execution_options(isolation_level="AUTOCOMMIT")
    logger.debug(f"-createEngine(), engine={engine}")
    return engine


@staticmethod
def createDatabase(engine: Engine) -> None:
    """ Creates the database. """
    logger.debug(f"+createDatabase({engine})")
    # self.session = Session()
    # Using our table metadata and our engine, we can generate our schema at once in our target SQLite
    # database, using a method called 'MetaData.create_all()':
    # self.metadata = MetaData()
    # MetaData.create_all(BaseSchema, bind=self.engine)
    # self.metadata.create_all(self.engine)
    # AbstractEntity.metadata.create_all(bind=self.engine)
    try:
        BaseSchema.metadata.create_all(bind=engine)
    except Exception as ex:
        logger.error(f"Error while creating database! Exception={ex}")

    logger.debug(f"-createDatabase(), engine={engine}")


# 'click.command()' defines a command line command called init-db that calls the 'init_db' function and shows a success
# message to the user. You can read Command Line Interface to learn more about writing commands.
@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    click.echo('Initializing the database ...')
    db = SQLite3Connector()
    db.init(None)
    # db.init_db()
    click.echo('Database is successfully initialized.')


# def init_app(app):
#     # app.teardown_appcontext() tells Flask to call that function when cleaning up after returning the response.
#     app.teardown_appcontext(SQLite3Database().close_connection())
#     # app.cli.add_command() adds a new command that can be called with the flask command.
#     app.cli.add_command(init_db_command)

# Define Constants
KEY_CONNECTION = 'connection'
KEY_POOL_NAME = 'sqlite3_pool'
SQLITE_PREFIX = 'sqlite:///'


class DatabaseConnector(object):
    """Database Connector"""

    def __init__(self):
        current_app.logger.debug("Initializing Connector ...")
        self.UTF_8 = 'UTF-8'

    def init(self, app: Flask = None):
        current_app.logger.debug("Initializing Connector with application ...")

    def init_db(self, configs: dict = None):
        current_app.logger.debug("Initializing database ...")


class SQLite3Connector(DatabaseConnector):
    """SQLite is a C-language library that implements a small, fast, self-contained, high-reliability, full-featured,
    SQL database engine. SQLite is the most used database engine in the world.
    """

    def __init__(self):
        """Initialize"""
        # current_app.logger.debug("Initializing SQLite3 Connector ...")
        self.app = None
        self.pool = None
        self.db_name: str = None
        self.db_user_name = None
        self.db_password = None
        self.db_uri = None
        self.engine: Engine = None
        # self.metadata = None
        # self.session = None

        # paths
        self.cur_dir = Path(__file__).parent
        # current_app.logger.debug(f"cur_dir:{self.cur_dir}")
        self.data_path = self.cur_dir.joinpath("data")
        # current_app.logger.debug(f"data_path:{self.data_path}")

    def get_connection(self):
        """Get Connection"""
        current_app.logger.debug(f"get_connection(), db_name: {self.db_name}, db_password: {self.db_password}")
        return sqlite3.connect(self.db_name, detect_types=sqlite3.PARSE_DECLTYPES)

    def init(self, app):
        """Initialize App Context"""
        self.app = app
        with self.app.app_context():
            current_app.logger.debug(f"Initializing App Context for {app} ...")
        self._init_configs()
        # 'app.teardown_appcontext()' tells Flask to call that function when cleaning up after returning the response.
        # self.app.teardown_appcontext(self.close_connection())

        # self.create_pool()
        # app.cli.add_command() adds a new command that can be called with the flask command.
        # self.app.cli.add_command(self.init_db)

    def _init_configs(self):
        """Initializes Configs"""
        with self.app.app_context():
            current_app.logger.debug(f"Initializing Configs ...")
            # current_app.logger.debug(f"current_app: {current_app}, current_app.config: {current_app.config}")
            # read db-name from app's config
            if not self.db_name:
                self.db_name = self.app.config.get("DB_NAME")

            current_app.logger.debug(f"self.db_name={self.db_name}")
            if self.db_name and not self.db_name.endswith(".db"):
                self.db_name = '.'.join([self.db_name, "db"])

            # build db uri
            self.db_uri = ''.join([SQLITE_PREFIX, self.db_name])
            self.db_password = self.app.config.get("DB_PASSWORD")
            current_app.logger.debug(f"db_name={self.db_name}, db_password={self.db_password}, db_uri={self.db_uri}")

    def init_db(self, configs: dict = None):
        """Initializes the database"""
        with self.app.app_context():
            current_app.logger.debug(f"Initializing Database. configs={configs}")
            dbType = configs.get(KeyEnum.DB_TYPE.name)
            current_app.logger.debug(f"dbType={dbType}")
            if dbType and KeyEnum.equals(KeyEnum.SQLALCHEMY, dbType):
                """Initializes the SQLAlchemy database"""
                # Set up the SQLAlchemy Database to be a local file 'posts.db'
                self.app.config['SQLALCHEMY_DATABASE_URI'] = self.db_uri
                # SQLAlchemy DB Creation
                self.engine = createEngine(self.db_uri, debug=True)
                createDatabase(self.engine)

            else:
                """Initializes the SQLite Database"""
                #  current_app.logger.debug(f"current_app: {current_app}, current_app.config: {current_app.config}")
                # read db-name from app's config
                try:
                    connection = self.open_connection()
                    # read the db-schema file and prepare db
                    with open(self.data_path.joinpath('schema.sql'), encoding='UTF_8') as schema_file:
                        connection.executescript(schema_file.read())

                except Exception as ex:
                    current_app.logger.debug(f'Error initializing database! Error:{ex}')
                finally:
                    # close the connection
                    self.close_connection()

    def open_connection(self):
        """Opens the database connection"""
        with self.app.app_context():
            current_app.logger.debug("Opening database connection ...")
            if not hasattr(g, 'connection'):
                current_app.logger.debug(f"db_name:{self.db_name}, db_password:{self.db_password}")
                g.connection = self.get_connection()
                current_app.logger.debug(f"g.connection: {g.connection}")
                g.connection.row_factory = sqlite3.Row
                # g.connection.cursor(dictionary=True)
                # g.connection.autocommit = False

            return g.connection

        return None

    def close_connection(self, connection=None, error=None):
        """Closes the database connection"""
        with self.app.app_context():
            if hasattr(g, 'connection'):
                try:
                    try:
                        if error:
                            g.connection.rollback()
                            current_app.logger.debug('Rollback occurred due to an error!')

                        # closing the cursor
                        # g.cursor.close()
                    except Exception as ex:
                        current_app.logger.debug(f'Error while rollback/closing the cursor! Error:{ex}')
                    finally:
                        g.connection.close()
                except Exception as ex:
                    current_app.logger.debug(f'Error while closing the connection! Error:{ex}')
            else:
                current_app.logger.debug('No active connection!')

    def save(self, instance):
        """Saves the instance using context manager"""
        current_app.logger.debug(f"+save(), instance={instance}")
        with Session(self.engine) as session:
            try:
                session.begin()
                session.add(instance)
            except Exception as ex:
                current_app.logger.error(f"Failed transaction with error:{ex}")
                session.rollback()
                raise ex
            else:
                session.commit()
                current_app.logger.debug("Persisted a instance successfully!")
        current_app.logger.debug(f"-save()")

    def save_all(self, instances: Iterable[object]):
        """Saves the instances using context manager"""
        current_app.logger.debug(f"+save_all(), instances={instances}")
        with Session(self.engine) as session:
            try:
                session.begin()
                session.add_all(instances)
            except Exception as ex:
                current_app.logger.error(f"Failed transaction with error:{ex}")
                session.rollback()
                raise ex
            else:
                session.commit()
                current_app.logger.debug(f"Persisted [{len(instances)}] instances successfully!")
        current_app.logger.debug(f"-save_all()")

    def select(self, entity: BaseSchema):
        current_app.logger.info(f"select => entity={entity}")
        with Session(self.engine) as session:
            return session.query(entity).first()

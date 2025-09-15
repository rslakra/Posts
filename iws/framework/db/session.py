#
# Author: Rohtash Lakra
#
# https://docs.sqlalchemy.org/en/20/orm/session_basics.html#when-do-i-construct-a-session-when-do-i-commit-it-and-when-do-i-close-it
# 
import logging
from typing import Iterable

from sqlalchemy import select
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class SessionManager:

    def __init__(self, engine, metadata):
        """Initialize Session Manager"""
        self.pool = None
        self.db_uri = None
        self.engine = engine
        self.metadata = metadata
        self.session = None

    def save(self, instance):
        """Saves the instance using context manager"""
        logger.debug(f"+save(), instance={instance}")
        with Session(self.engine) as session:
            session.begin()
            try:
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
            session.begin()
            try:
                session.add_all(instances)
            except Exception as ex:
                logger.error(f"Failed transaction with error:{ex}")
                session.rollback()
                raise ex
            else:
                session.commit()
                logger.debug(f"Persisted [{len(instances)}] instances successfully!")
        logger.debug(f"-save_all()")

    def select_all(self, instance_class, *columns, **filters):
        """Selects all the instances using context manager"""
        logger.info(f"select_all(), instance_class={instance_class}, columns={columns}")
        with Session(self.engine) as session:
            session.begin()
            try:
                if filters:
                    statement = select(instance_class).filter_by(filters)
                else:
                    statement = select(instance_class)
            except Exception as ex:
                logger.error(f"Failed transaction with error:{ex}")
                session.rollback()
                raise ex
            else:
                rows = session.execute(statement).all()
        logger.info(f"select_all(), rows={rows}")
        return rows

    def select(self, instance_class, *columns, **filters):
        """Selects the instance using context manager"""
        logger.info(f"select(), instance_class={instance_class}, columns={columns}")
        with Session(self.engine) as session:
            session.begin()
            try:
                if filters:
                    statement = select(instance_class).filter_by(filters)
                else:
                    statement = select(instance_class)
            except Exception as ex:
                logger.error(f"Failed transaction with error:{ex}")
                session.rollback()
                raise ex
            else:
                row = session.execute(statement).first()

        logger.info(f"select(), row={row}")
        return row

    def delete(self, instance):
        """Deletes the instance using context manager"""
        logger.debug(f"+delete(), instance={instance}")
        with Session(self.engine) as session:
            session.begin()
            try:
                session.delete(instance)
            except Exception as ex:
                logger.error(f"Failed transaction with error:{ex}")
                session.rollback()
                raise ex
            else:
                session.commit()
                logger.debug("Persisted a instance successfully!")
        logger.debug(f"-delete()")

    def delete_all(self, instances: Iterable[object]):
        """Deletes all the instances using context manager"""
        logger.debug(f"+delete_all(), instances={instances}")
        with Session(self.engine) as session:
            session.begin()
            try:
                for instance in instances:
                    session.delete(instance)
            except Exception as ex:
                logger.error(f"Failed delete transaction with error:{ex}")
                session.rollback()
                raise ex
            else:
                session.commit()
                logger.debug(f"Deleted [{len(instances)}] instances successfully!")
        logger.debug(f"-delete_all()")

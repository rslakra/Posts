#
# Author: Rohtash Lakra
#
import logging
from typing import Iterable, Dict, Any
from typing import List, Optional

from sqlalchemy import text, Engine
from sqlalchemy.exc import NoResultFound, MultipleResultsFound, SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.orm.mapper import Mapper

from framework.orm.repository import AbstractRepository
from framework.orm.sqlalchemy.schema import BaseSchema

logger = logging.getLogger(__name__)


class SqlAlchemyRepository(AbstractRepository):
    """The base repository of all ORM repositories."""

    def __init__(self, engine: Engine):
        super().__init__(engine=engine)

    def save(self, instance: BaseSchema) -> BaseSchema:
        """Returns records by filter or empty list"""
        logger.debug(f"+{self.__class__.__name__}.save({instance})")
        if instance is not None:
            with Session(bind=self.get_engine(), expire_on_commit=False) as session:
                try:
                    session.add(instance)
                    # Commit:
                    # The pending changes above are flushed via flush(), the Transaction is committed, the Connection
                    # object closed and discarded, the underlying DBAPI connection returned to the connection pool.
                    session.commit()
                    logger.debug(f"Persisted a instance successfully!")
                except Exception as ex:
                    logger.error(f"Transaction failed while saving record! Error={ex}")
                    # on rollback, the same closure of state as that of commit proceeds.
                    session.rollback()
                    raise ex
                except:
                    logger.error(f"Transaction failed while saving record!")
                    # on rollback, the same closure of state as that of commit proceeds.
                    session.rollback()
                    raise
                else:
                    # Refresh to get any other DB-generated values
                    session.refresh(instance)
                finally:
                    # close the Session.
                    # This will expunge any remaining objects as well as reset any existing 'SessionTransaction' state.
                    # Neither of these steps are usually essential.
                    # However, if the commit() or rollback() itself experienced an unanticipated internal failure
                    # (such as due to a mis-behaved user-defined event handler), .close() will ensure that invalid state
                    # is removed.
                    session.close()
        else:
            logger.warning(f"No instance provided to persist!")

        logger.debug(f"-{self.__class__.__name__}.save(), instance={instance}")
        return instance

    def save_all(self, instances: Iterable[BaseSchema]) -> None:
        """Returns records by filter or empty list"""
        logger.debug(f"+{self.__class__.__name__}.save_all({instances})")
        if instances is not None:
            with Session(bind=self.get_engine(), expire_on_commit=False) as session:
                try:
                    session.add_all(instances)
                    # Commit:
                    # The pending changes above are flushed via flush(), the Transaction is committed, the Connection
                    # object closed and discarded, the underlying DBAPI connection returned to the connection pool.
                    session.commit()
                    logger.debug(f"Persisted [{len(instances)}] instances successfully!")
                except Exception as ex:
                    logger.error(f"Transaction failed while saving record! Error={ex}")
                    # on rollback, the same closure of state as that of commit proceeds.
                    session.rollback()
                    raise ex
                except:
                    logger.error(f"Transaction failed while saving records!")
                    # on rollback, the same closure of state as that of commit proceeds.
                    session.rollback()
                    raise
                finally:
                    # close the Session.
                    # This will expunge any remaining objects as well as reset any existing 'SessionTransaction' state.
                    # Neither of these steps are usually essential.
                    # However, if the commit() or rollback() itself experienced an unanticipated internal failure
                    # (such as due to a mis-behaved user-defined event handler), .close() will ensure that invalid state
                    # is removed.
                    session.close()
        else:
            logger.warning(f"No instances provided to persist!")

        logger.debug(f"-{self.__class__.__name__}.save_all()")

    def filter(self, filters: Dict[str, Any]) -> List[Optional[BaseSchema]]:
        """Filters the records of the provided table by parses filters dict.

        Parameters:
        - filters (Dict[str, Any]): The filter fields mappings that represents the db schema filters.
        - return: Optional[BaseSchema]
        """

        pass

    def findById(self, schemaObject: BaseSchema, id: int) -> Optional[BaseSchema]:
        """Finds the record by id in the provided table and parses object's dict.

        Parameters:
        - schemaObject (BaseSchema): The schema class that represents the db schema.
        - id (int): id of the object

        - return: Optional[BaseSchema]
        """
        logger.debug(f"+{self.__class__.__name__}.findById({schemaObject}, {id})")
        with Session(bind=self.get_engine(), expire_on_commit=False) as session:
            try:
                schemaObject = session.query(schemaObject).filter(schemaObject.id == id).one()
                # rows = session.execute(text(query)).fetchall()
                # results = [row._asdict() for row in rows]
                logger.debug(f"Loaded a [{type(schemaObject)}] record. schemaObject={schemaObject}")

                # Commit:
                # The pending changes above are flushed via flush(), the Transaction is committed, the Connection
                # object closed and discarded, the underlying DBAPI connection returned to the connection pool.
                session.commit()
            except NoResultFound as ex:
                logger.error(f"NoResultFound while loading [{type(schemaObject)}]! Error={ex}")
                # on rollback, the same closure of state as that of commit proceeds.
                session.rollback()
                raise ex
            except MultipleResultsFound as ex:
                logger.error(f"MultipleResultsFound while loading [{type(schemaObject)}]! Error={ex}")
                # on rollback, the same closure of state as that of commit proceeds.
                session.rollback()
                raise ex
            except Exception as ex:
                logger.error(f"Exception while loading [{type(schemaObject)}]! Error={ex}")
                # on rollback, the same closure of state as that of commit proceeds.
                session.rollback()
                raise ex
            except:
                # on rollback, the same closure of state as that of commit proceeds.
                logger.error(f"Exception while loading [{type(schemaObject)}]!")
                session.rollback()
                raise
            finally:
                # close the Session.
                # This will expunge any remaining objects as well as reset any existing 'SessionTransaction' state.
                # Neither of these steps are usually essential.
                # However, if the commit() or rollback() itself experienced an unanticipated internal failure
                # (such as due to a mis-behaved user-defined event handler), .close() will ensure that invalid state
                # is removed.
                session.close()

        logger.debug(f"-{self.__class__.__name__}.findById(), schemaObject={schemaObject}")
        return schemaObject

    def findAll(self, schemaObject: BaseSchema, filters: Dict[str, Any]) -> List[Optional[BaseSchema]]:
        """Returns the records by filter or empty list"""
        logger.debug(f"+{self.__class__.__name__}.findAll({schemaObject}, {filters})")
        schemaObjects = None
        # verbose version of what a context manager will do
        with Session(bind=self.get_engine(), expire_on_commit=False) as session:
            try:
                if filters:
                    schemaObjects = session.query(schemaObject).filter_by(**filters).all()
                else:
                    schemaObjects = session.query(schemaObject).all()

                logger.debug(f"Loaded [{len(schemaObjects)}] records. schemaObjects={schemaObjects}")

                # Commit:
                # The pending changes above are flushed via flush(), the Transaction is committed, the Connection
                # object closed and discarded, the underlying DBAPI connection returned to the connection pool.
                session.commit()
            except NoResultFound as ex:
                logger.error(f"NoResultFound while loading permissions! Error={ex}")
                # on rollback, the same closure of state as that of commit proceeds.
                session.rollback()
                raise ex
            except MultipleResultsFound as ex:
                logger.error(f"MultipleResultsFound while loading permissions! Error={ex}")
                # on rollback, the same closure of state as that of commit proceeds.
                session.rollback()
                raise ex
            except Exception as ex:
                logger.error(f"Exception while loading permissions! Error={ex}")
                # on rollback, the same closure of state as that of commit proceeds.
                session.rollback()
                raise ex
            except:
                # on rollback, the same closure of state as that of commit proceeds.
                logger.error(f"Exception while loading permissions!")
                session.rollback()
                raise
            finally:
                # close the Session.
                # This will expunge any remaining objects as well as reset any existing 'SessionTransaction' state.
                # Neither of these steps are usually essential.
                # However, if the commit() or rollback() itself experienced an unanticipated internal failure
                # (such as due to a mis-behaved user-defined event handler), .close() will ensure that invalid state
                # is removed.
                session.close()

        logger.debug(f"-{self.__class__.__name__}.findAll(), schemaObjects={schemaObjects}")
        return schemaObjects

    def updateObjects(self, table: str, update_json=[]) -> Optional[List[dict]]:
        """Finds rows of the provided table from the database and parses as list of dict.

        :param Engine engine: Database engine to handle raw SQL queries.
        :param str table: table name which records to fetch.

        :return: Optional[List[dict]]
        """
        logger.debug(f"{self.__class__.__name__}.updateObjects({table}, {update_json})")
        query = f'UPDATE {table} {self.build_update_set_fields(update_json)}'
        with Session(self.get_engine()) as session:
            try:
                rows = session.execute(text(query), ).fetchall()
                logger.debug(f"Updated [{rows.rowcount}] rows => {rows}")
                return rows
            except SQLAlchemyError as ex:
                logger.error(f"SQLAlchemyError while updating records! Error={ex}")
                session.rollback()
            except Exception as ex:
                logger.error(f"Exception while updating records! Error={ex}")
                session.rollback()
            else:
                session.commit()

    def update(self, mapper: Mapper[BaseSchema], mappings: List[BaseSchema]) -> List[Optional[BaseSchema]]:
        """Updates an instance into database via the ORM flush process."""
        logger.debug(f"+{self.__class__.__name__}.update(), mapper={mapper}, mappings={mappings}")
        if mappings is not None:
            with Session(self.get_engine()) as session:
                try:
                    session.bulk_update_mappings(mapper, mappings)
                    session.flush()
                    session.commit()
                    logger.debug(f"Persisted a instance successfully!")
                except Exception as ex:
                    logger.error(f"Failed transaction with error:{ex}")
                    session.rollback()
                else:
                    # Refresh to get any other DB-generated values
                    session.refresh(mappings)
        else:
            logger.warning(f"No instance provided to update!")

        logger.debug(f"-{self.__class__.__name__}.update(), mappings={mappings}")
        return mappings

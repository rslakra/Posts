#
# Author: Rohtash Lakra
#
import logging
from typing import List, Optional, Dict, Any

from sqlalchemy import update, func
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.orm import Session

from framework.orm.sqlalchemy.repository import SqlAlchemyRepository
from framework.orm.sqlalchemy.schema import BaseSchema
from globals import connector
from rest.role.schema import RoleSchema, PermissionSchema

logger = logging.getLogger(__name__)


class RoleRepository(SqlAlchemyRepository):
    """The RoleRepository handles a schema-centric database persistence for roles."""

    def __init__(self):
        super().__init__(engine=connector.engine)

    # @override
    def filter(self, filters: Dict[str, Any]) -> List[Optional[RoleSchema]]:
        """Returns records by filter or empty list"""
        logger.debug(f"+findByFilter({filters})")
        schemaObjects = None
        # verbose version of what a context manager will do
        with Session(bind=self.get_engine(), expire_on_commit=False) as session:
            # session.begin()
            try:
                if filters and filters is not None:
                    if len(filters) == 1 and "id" in filters.keys() and isinstance(filters.get("id"), list):
                        schemaObjects = session.query(RoleSchema).filter(RoleSchema.id.in_(filters.get("id"))).all()
                    else:
                        logger.debug(f"filters={filters}, filters={filters.keys()}")
                        schemaObjects = session.query(RoleSchema).filter_by(**filters).all()
                else:
                    schemaObjects = session.query(RoleSchema).all()

                logger.debug(f"Loaded [{len(schemaObjects)}] roles. schemaObjects={schemaObjects}")

                # Commit:
                # The pending changes above are flushed via flush(), the Transaction is committed, the Connection
                # object closed and discarded, the underlying DBAPI connection returned to the connection pool.
                session.commit()
            except NoResultFound as ex:
                logger.error(f"NoResultFound while loading roles! Error={ex}")
                # on rollback, the same closure of state as that of commit proceeds.
                session.rollback()
                raise ex
            except MultipleResultsFound as ex:
                logger.error(f"MultipleResultsFound while loading roles! Error={ex}")
                # on rollback, the same closure of state as that of commit proceeds.
                session.rollback()
                raise ex
            except Exception as ex:
                logger.error(f"Exception while loading roles! Error={ex}")
                # on rollback, the same closure of state as that of commit proceeds.
                session.rollback()
                raise ex
            except:
                logger.error(f"Exception while loading roles!")
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

        logger.debug(f"-findByFilter(), schemaObjects={schemaObjects}")
        return schemaObjects

    def findByName(self, name: str) -> RoleSchema:
        logger.debug(f"+findByName({name})")
        results = List[Optional[RoleSchema]]
        with Session(self.get_engine()) as session:
            try:
                results = session.query(RoleSchema).filter(RoleSchema.name == name).all()
                logger.debug(f"Loaded [{len(results)}] roles => results={results}")
            except NoResultFound as ex:
                logger.error(f"NoResultFound while loading role by name! Error={ex}")
                # session.rollback()
                raise ex
            except MultipleResultsFound as ex:
                logger.error(f"MultipleResultsFound while loading role by name! Error={ex}")
                # session.rollback()
                raise ex
            except Exception as ex:
                logger.error(f"Exception while loading role by name! Error={ex}")
                # session.rollback()
                raise ex

        logger.info(f"-findByName(), results={results}")
        return results

    def update(self, schemaObject: RoleSchema) -> int:
        logger.debug(f"+update({schemaObject})")
        with Session(bind=self.get_engine(), expire_on_commit=False) as session:
            try:
                if not isinstance(schemaObject, BaseSchema):
                    raise ValueError(f"Invalid schemaObject type={type(schemaObject)}")

                # update updated_at to current datetime value
                schemaObject.updated_at = func.now()
                results = session.execute(
                    update(RoleSchema)
                    .values(schemaObject.to_json())
                    .where(RoleSchema.id == schemaObject.id)
                ).rowcount
                logger.debug(f"Updated [{results}] role.")

                session.commit()
            except NoResultFound as ex:
                logger.error(f"NoResultFound while updating role! Error={ex}")
                session.rollback()
                raise ex
            except MultipleResultsFound as ex:
                logger.error(f"MultipleResultsFound while updating role! Error={ex}")
                session.rollback()
                raise ex
            except Exception as ex:
                logger.error(f"Exception while updating role! Error={ex}")
                session.rollback()
                raise ex

        logger.info(f"-update(), results={results}")
        return results

    def delete(self, filters: Dict[str, Any]) -> None:
        logger.debug(f"+delete({filters})")
        with Session(bind=self.get_engine(), expire_on_commit=False) as session:
            try:
                roleSchema = session.query(RoleSchema).filter_by(**filters).one()
                logger.debug(f"Deleting roleSchema={roleSchema}")
                session.delete(roleSchema)
                logger.info("Role is successfully deleted.")
                session.commit()
            except NoResultFound as ex:
                logger.error(f"NoResultFound while deleting roles! Error={ex}")
                session.rollback()
                raise ex
            except MultipleResultsFound as ex:
                logger.error(f"MultipleResultsFound while deleting roles! Error={ex}")
                session.rollback()
                raise ex
            except Exception as ex:
                logger.error(f"Exception while deleting roles! Error={ex}")
                session.rollback()
                raise ex

        logger.info(f"-delete()")

    def bulkDelete(self, ids: list[int]) -> None:
        logger.debug(f"+bulkDelete({ids})")
        with Session(bind=self.get_engine(), expire_on_commit=False) as session:
            try:
                schemaObjects = self.filter({"id": ids})
                for schemaObject in schemaObjects:
                    logger.debug(f"Deleting role with id=[{schemaObject.id}]")
                    session.delete(schemaObject)

                logger.debug(f"Deleted [{len(schemaObjects)}] roles successfully.")
                session.commit()
            except NoResultFound as ex:
                logger.error(f"NoResultFound while bulk deleting roles! Error={ex}")
                session.rollback()
                raise ex
            except MultipleResultsFound as ex:
                logger.error(f"MultipleResultsFound while bulk deleting roles! Error={ex}")
                session.rollback()
                raise ex
            except Exception as ex:
                logger.error(f"Exception while bulk deleting roles! Error={ex}")
                session.rollback()
                raise ex

        logger.info(f"-bulkDelete()")


class PermissionRepository(SqlAlchemyRepository):
    """The PermissionRepository handles a schema-centric database persistence for permissions."""

    def __init__(self):
        super().__init__(engine=connector.engine)

    # @override
    def filter(self, filters: Dict[str, Any]) -> List[Optional[PermissionSchema]]:
        """Returns records by filter or empty list"""
        logger.debug(f"+findByFilter({filters})")
        schemaObjects = None
        # verbose version of what a context manager will do
        with Session(bind=self.get_engine(), expire_on_commit=False) as session:
            try:
                if filters:
                    if len(filters) == 1 and "id" in filters.keys() and isinstance(filters.get("id"), list):
                        schemaObjects = session.query(PermissionSchema).filter(
                            PermissionSchema.id.in_(filters.get("id"))).all()
                    else:
                        schemaObjects = session.query(PermissionSchema).filter_by(**filters).all()
                else:
                    schemaObjects = session.query(PermissionSchema).all()

                logger.debug(f"Loaded [{len(schemaObjects)}] permissions. schemaObjects={schemaObjects}")

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

        logger.debug(f"-findByFilter(), schemaObjects={schemaObjects}")
        return schemaObjects

    def update(self, schemaObject: PermissionSchema) -> PermissionSchema:
        logger.debug(f"+update({schemaObject})")
        with Session(bind=self.get_engine(), expire_on_commit=False) as session:
            try:
                schemaObject.updated_at = func.now()
                results = session.execute(
                    update(PermissionSchema)
                    .values(schemaObject.to_json())
                    .where(PermissionSchema.id == schemaObject.id)
                ).rowcount
                logger.debug(f"Updated [{results}] rows.")

                session.commit()
            except NoResultFound as ex:
                logger.error(f"NoResultFound while updating permission! Error={ex}")
                session.rollback()
                raise ex
            except MultipleResultsFound as ex:
                logger.error(f"MultipleResultsFound while updating permission! Error={ex}")
                session.rollback()
                raise ex
            except Exception as ex:
                logger.error(f"Exception while updating permission! Error={ex}")
                session.rollback()
                raise ex

        logger.info(f"-update(), results={results}")
        return results

    def delete(self, filters: Dict[str, Any]) -> None:
        logger.debug(f"+delete({filters})")
        with Session(bind=self.get_engine(), expire_on_commit=False) as session:
            try:
                permissionSchema = session.query(PermissionSchema).filter_by(**filters).one()
                logger.debug(f"Deleting permissionSchema={permissionSchema}")
                session.delete(permissionSchema)
                logger.info("Permission is successfully deleted.")
                session.commit()
            except NoResultFound as ex:
                logger.error(f"NoResultFound while deleting permissions! Error={ex}")
                session.rollback()
                raise ex
            except MultipleResultsFound as ex:
                logger.error(f"MultipleResultsFound while deleting permissions! Error={ex}")
                session.rollback()
                raise ex
            except Exception as ex:
                logger.error(f"Exception while updating deleting permissions! Error={ex}")
                session.rollback()
                raise ex

        logger.info(f"-delete()")

    def bulkDelete(self, ids: list[int]) -> None:
        logger.debug(f"+bulkDelete({ids})")
        with Session(bind=self.get_engine(), expire_on_commit=False) as session:
            try:
                schemaObjects = self.filter({"id": ids})
                for schemaObject in schemaObjects:
                    logger.debug(f"Deleting permission with id=[{schemaObject.id}]")
                    session.delete(schemaObject)

                logger.debug(f"Deleted [{len(schemaObjects)}] permissions successfully.")
                session.commit()
            except NoResultFound as ex:
                logger.error(f"NoResultFound while bulk deleting permissions! Error={ex}")
                session.rollback()
                raise ex
            except MultipleResultsFound as ex:
                logger.error(f"MultipleResultsFound while bulk deleting permissions! Error={ex}")
                session.rollback()
                raise ex
            except Exception as ex:
                logger.error(f"Exception while deleting bulk permissions! Error={ex}")
                session.rollback()
                raise ex

        logger.info(f"-bulkDelete()")

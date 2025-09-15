#
# Author: Rohtash Lakra
#
import logging
from typing import List, Optional, Dict, Any

from sqlalchemy import update, func
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.orm import Session

from framework.orm.sqlalchemy.repository import SqlAlchemyRepository
from globals import connector
from rest.contact.schema import ContactSchema

logger = logging.getLogger(__name__)


class ContactRepository(SqlAlchemyRepository):
    """The ContactRepository handles a schema-centric database persistence for contacts."""

    def __init__(self):
        super().__init__(engine=connector.engine)

    # @override
    def filter(self, filters: Dict[str, Any]) -> List[Optional[ContactSchema]]:
        """Returns records by filter or empty list"""
        logger.debug(f"+findByFilter({filters})")
        contactSchemas = None
        # verbose version of what a context manager will do
        with Session(bind=self.get_engine(), expire_on_commit=False) as session:
            # session.begin()
            try:
                if filters:
                    contactSchemas = session.query(ContactSchema).filter_by(**filters).all()
                else:
                    contactSchemas = session.query(ContactSchema).all()

                logger.debug(f"Loaded [{len(contactSchemas)}] rows => contactSchemas={contactSchemas}")

                # Commit:
                # The pending changes above are flushed via flush(), the Transaction is committed, the Connection
                # object closed and discarded, the underlying DBAPI connection returned to the connection pool.
                session.commit()
            except NoResultFound as ex:
                logger.error(f"NoResultFound while loading records! Error={ex}")
                # on rollback, the same closure of state as that of commit proceeds.
                session.rollback()
                raise ex
            except MultipleResultsFound as ex:
                logger.error(f"MultipleResultsFound while loading records! Error={ex}")
                # on rollback, the same closure of state as that of commit proceeds.
                session.rollback()
                raise ex
            except Exception as ex:
                logger.error(f"Exception while loading records! Error={ex}")
                # on rollback, the same closure of state as that of commit proceeds.
                session.rollback()
                raise ex
            except:
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

        logger.debug(f"-findByFilter(), contactSchemas={contactSchemas}")
        return contactSchemas

    def update(self, contactSchema: ContactSchema) -> ContactSchema:
        logger.debug(f"+update({contactSchema})")
        with Session(bind=self.get_engine(), expire_on_commit=False) as session:
            try:
                contactSchema.updated_at = func.now()
                results = session.execute(
                    update(ContactSchema)
                    .values(contactSchema.to_json())
                    .where(ContactSchema.id == contactSchema.id)
                ).rowcount
                logger.debug(f"Updated [{results}] rows.")

                session.commit()
            except NoResultFound as ex:
                logger.error(f"NoResultFound while updating records! Error={ex}")
                session.rollback()
                raise ex
            except MultipleResultsFound as ex:
                logger.error(f"MultipleResultsFound while updating records! Error={ex}")
                session.rollback()
                raise ex
            except Exception as ex:
                logger.error(f"Exception while updating records! Error={ex}")
                session.rollback()
                raise ex

        logger.info(f"-update(), results={results}")
        return results

    def delete(self, filters: Dict[str, Any]) -> None:
        logger.debug(f"+delete({filters})")
        with Session(bind=self.get_engine(), expire_on_commit=False) as session:
            try:
                contactSchema = session.query(ContactSchema).filter_by(**filters).one()
                logger.debug(f"contactSchema={contactSchema}")
                session.delete(contactSchema)
                logger.debug("Record is successfully deleted.")
                session.commit()
            except NoResultFound as ex:
                logger.error(f"NoResultFound while updating records! Error={ex}")
                session.rollback()
                raise ex
            except MultipleResultsFound as ex:
                logger.error(f"MultipleResultsFound while updating records! Error={ex}")
                session.rollback()
                raise ex
            except Exception as ex:
                logger.error(f"Exception while updating records! Error={ex}")
                session.rollback()
                raise ex

        logger.info(f"-delete()")

    def bulkDelete(self, ids: list[int]) -> None:
        logger.debug(f"+bulkDelete({ids})")
        with Session(bind=self.get_engine(), expire_on_commit=False) as session:
            try:
                contactSchemas = self.filter({"id": ids})
                for contactSchema in contactSchemas:
                    logger.debug(f"Deleting role with id=[{contactSchema.id}]")
                    session.delete(contactSchema)

                logger.debug(f"Deleted [{len(contactSchemas)}] rows successfully.")
                session.commit()
            except NoResultFound as ex:
                logger.error(f"NoResultFound while updating records! Error={ex}")
                session.rollback()
                raise ex
            except MultipleResultsFound as ex:
                logger.error(f"MultipleResultsFound while updating records! Error={ex}")
                session.rollback()
                raise ex
            except Exception as ex:
                logger.error(f"Exception while updating records! Error={ex}")
                session.rollback()
                raise ex

        logger.info(f"-bulkDelete()")

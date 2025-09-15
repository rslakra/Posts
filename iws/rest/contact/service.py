#
# Author: Rohtash Lakra
#
import logging
from typing import List, Optional, Dict, Any

from framework.exception import DuplicateRecordException, ValidationException, NoRecordFoundException
from framework.http import HTTPStatus
from framework.orm.pydantic.model import BaseModel
from framework.orm.sqlalchemy.schema import SchemaOperation
from framework.service import AbstractService
from rest.contact.mapper import ContactMapper
from rest.contact.model import Contact
from rest.contact.repository import ContactRepository

logger = logging.getLogger(__name__)


class ContactService(AbstractService):

    def __init__(self):
        logger.debug("ContactService()")
        super().__init__()
        self.repository = ContactRepository()

    def validate(self, operation: SchemaOperation, contact: Contact) -> None:
        logger.debug(f"+validate({operation}, {contact})")
        # super().validate(operation, contact)
        errorMessages = []

        # validate the object
        if not contact:
            errorMessages.append("'Contact' is not fully defined!")

        match operation.name:
            case SchemaOperation.CREATE.name:
                # validate the required fields
                if not contact.first_name:
                    errorMessages.append("Contact 'first_name' is required!")
                if not contact.last_name:
                    errorMessages.append("Contact 'last_name' is required!")
                if not contact.country:
                    errorMessages.append("Contact 'country' is required!")
                if not contact.subject:
                    errorMessages.append("Contact 'subject' is required!")

            case SchemaOperation.UPDATE.name:
                if not contact.id:
                    errorMessages.append("Contact 'id' is required!")

        # throw an error if any validation error
        if errorMessages and len(errorMessages) > 0:
            error = ValidationException(httpStatus=HTTPStatus.INVALID_DATA, messages=errorMessages)
            logger.debug(f"{type(error)} = exception={error}")
            raise error

        logger.debug(f"-validate()")

    # @override
    def findByFilter(self, filters: Dict[str, Any]) -> List[Optional[BaseModel]]:
        logger.debug(f"+findByFilter({filters})")
        contactSchemas = self.repository.filter(filters)
        contactModels = []
        for contactSchema in contactSchemas:
            contactModel = ContactMapper.fromSchema(contactSchema)
            contactModels.append(contactModel)

        logger.debug(f"-findByFilter(), contactModels={contactModels}")
        return contactModels

    # @override
    def existsByFilter(self, filters: Dict[str, Any]) -> bool:
        """Returns True if the records exist by filter otherwise False"""
        logger.debug(f"+existsByFilter({filters})")
        contactSchemas = self.repository.filter(filters)
        result = True if contactSchemas else False
        logger.debug(f"-existsByFilter(), result={result}")
        return result

    def validates(self, operation: SchemaOperation, contacts: List[Contact]) -> None:
        logger.debug(f"+validates({operation}, {contacts})")
        errorMessages = []

        # validate the object
        if not contacts:
            errorMessages.append('Roles is required!')

        for contact in contacts:
            self.validate(operation, contact)

        # throw an error if any validation error
        if errorMessages and len(errorMessages) > 0:
            error = ValidationException(httpStatus=HTTPStatus.INVALID_DATA, messages=errorMessages)
            logger.debug(f"{type(error)} = exception={error}")
            raise error

        logger.debug(f"-validates()")

    def create(self, contact: Contact) -> Contact:
        """Crates a new contact"""
        logger.debug(f"+create({contact})")
        if self.existsByFilter({"subject": contact.subject}):
            raise DuplicateRecordException(HTTPStatus.CONFLICT, f"[{contact.subject}] contact already exists!")

        # contact = self.repository.create(contact)
        contactSchema = ContactMapper.fromModel(contact)
        contactSchema = self.repository.save(contactSchema)
        if contactSchema and contactSchema.id is None:
            contactSchema = self.repository.filter({"subject": contact.subject})

        contact = ContactMapper.fromSchema(contactSchema)
        logger.debug(f"-create(), contact={contact}")
        return contact

    def bulkCreate(self, contacts: List[Contact]) -> List[Contact]:
        """Crates a new contact"""
        logger.debug(f"+bulkCreate({contacts})")
        results = []
        for contact in contacts:
            result = self.create(contact)
            results.append(result)

        logger.debug(f"-bulkCreate(), results={results}")
        return results

    def update(self, contact: Contact) -> Contact:
        """Updates the contact"""
        logger.debug(f"+update({contact})")
        if not self.existsByFilter({"id": contact.id}):
            raise NoRecordFoundException(HTTPStatus.NOT_FOUND, "Contact doesn't exist!")

        contactSchemas = self.repository.filter({"id": contact.id})
        contactSchema = contactSchemas[0]
        if contact.first_name and contactSchema.first_name != contact.first_name:
            contactSchema.first_name = contact.first_name

        if contact.last_name and contactSchema.last_name != contact.last_name:
            contactSchema.last_name = contact.last_name

        if contact.country and contactSchema.country != contact.country:
            contactSchema.country = contact.country

        if contact.subject and contactSchema.subject != contact.subject:
            contactSchema.subject = contact.subject

        self.repository.update(contactSchema)
        contactSchema = self.repository.filter({"id": contact.id})[0]
        contact = ContactMapper.fromSchema(contactSchema)
        logger.debug(f"-update(), contact={contact}")
        return contact

    def delete(self, id: int) -> None:
        logger.debug(f"+delete({id})")
        # check record exists by id
        filter = {"id": id}
        if self.existsByFilter(filter):
            self.repository.delete(filter)
        else:
            raise NoRecordFoundException(HTTPStatus.NOT_FOUND, "Contact doesn't exist!")

        logger.debug(f"-delete()")

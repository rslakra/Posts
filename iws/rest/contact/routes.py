#
# Author: Rohtash Lakra
#
import logging

from fastapi import Request
from fastapi.responses import JSONResponse

from rest.base import BaseRouter
from framework.exception import DuplicateRecordException, ValidationException, NoRecordFoundException
from framework.http import HTTPStatus
from framework.orm.pydantic.model import ResponseModel
from framework.orm.sqlalchemy.schema import SchemaOperation
from rest.contact.model import Contact
from rest.contact.service import ContactService
from rest.contact.v1 import bp as bp_contact_v1

logger = logging.getLogger(__name__)


class ContactRouter(BaseRouter):
    """ContactRouter handles CRUD operations for contact resources."""

    async def create(self, request: Request):
        """Create a contact."""
        logger.debug(f"+create() => request={request}, args={request.query_params}")
        try:
            body = await self.json_or_none(request)
            logger.debug(f"body={body}")
            contact = Contact(**body) if body is not None else None
            logger.debug(f"contact={contact}")
            contactService = ContactService()
            contactService.validate(SchemaOperation.CREATE, contact)
            contact = contactService.create(contact)
            logger.debug(f"contact={contact}")
            response = ResponseModel(status=HTTPStatus.CREATED.statusCode, message="Contact is successfully created.")
            response.addInstance(contact)
        except ValidationException as ex:
            response = ResponseModel.buildResponseWithException(ex)
        except DuplicateRecordException as ex:
            response = ResponseModel.buildResponseWithException(ex)
        except Exception as ex:
            response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

        logger.debug(f"-create() <= response={response}")
        return JSONResponse(status_code=response.status, content=response.to_json())

    async def bulkCreate(self, request: Request):
        """Create multiple contacts in one request."""
        logger.debug(f"+bulkCreate() => request={request}, args={request.query_params}")
        try:
            roles = []
            body = await self.json_or_none(request)
            if body is not None:
                logger.debug(f"type={type(body)}, body={body}")
                if isinstance(body, list):
                    roles = [Contact(**entry) for entry in body]
                elif isinstance(body, dict):
                    roles.append(Contact(**body))

            logger.debug(f"roles={roles}")
            contactService = ContactService()
            contactService.validates(SchemaOperation.CREATE, roles)
            roles = contactService.bulkCreate(roles)
            logger.debug(f"roles={roles}")
            response = ResponseModel(status=HTTPStatus.CREATED.statusCode, message="Roles are successfully created.")
            response.addInstances(roles)
        except ValidationException as ex:
            response = ResponseModel.buildResponseWithException(ex)
        except DuplicateRecordException as ex:
            response = ResponseModel.buildResponseWithException(ex)
        except Exception as ex:
            response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

        logger.debug(f"-bulkCreate() <= response={response}")
        return JSONResponse(status_code=response.status, content=response.to_json())

    async def get(self, request: Request):
        """Fetch contacts using optional query filters."""
        logger.debug(f"+get() => request={request}, args={request.query_params}")
        try:
            contactService = ContactService()
            roles = contactService.findByFilter(self.query_params(request))
            response = ResponseModel.buildResponse(HTTPStatus.OK)
            if roles:
                response.addInstances(roles)
            else:
                response.message = "No Records Exist!"
        except Exception as ex:
            response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

        logger.debug(f"-get() <= response={response}")
        return JSONResponse(status_code=response.status, content=response.to_json())

    async def update(self, request: Request):
        """Update an existing contact."""
        logger.debug(f"+update() => request={request}, args={request.query_params}")
        try:
            body = await self.json_or_none(request)
            contact = None
            if body is not None:
                logger.debug(f"body={body}")
                contact = Contact(**body)
                logger.debug(f"contact={contact}")

            contactService = ContactService()
            contactService.validate(SchemaOperation.UPDATE, contact)
            contact = contactService.update(contact)
            logger.debug(f"contact={contact}")
            response = ResponseModel(status=HTTPStatus.OK.statusCode, message="Contact is successfully updated.")
            response.addInstance(contact)
        except ValidationException as ex:
            response = ResponseModel.buildResponseWithException(ex)
        except NoRecordFoundException as ex:
            response = ResponseModel.buildResponseWithException(ex)
        except Exception as ex:
            response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

        logger.debug(f"-update() <= response={response}")
        return JSONResponse(status_code=response.status, content=response.to_json())

    async def delete(self, id: int, request: Request):
        """Delete a contact by id."""
        logger.debug(f"+delete({id}) => request={request}, args={request.query_params}")
        try:
            body = await self.json_or_none(request)
            if body is not None:
                logger.debug(f"body={body}")
                contact = Contact(**body)
                logger.debug(f"contact={contact}")

            contactService = ContactService()
            contactService.delete(id)
            response = ResponseModel(status=HTTPStatus.OK.statusCode, message="Contact is successfully deleted.")
        except NoRecordFoundException as ex:
            response = ResponseModel.buildResponseWithException(ex)
        except Exception as ex:
            response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

        logger.debug(f"-delete() <= response={response}")
        return JSONResponse(status_code=response.status, content=response.to_json())


contactRouter = ContactRouter()
bp_contact_v1.add_api_route("/", contactRouter.create, methods=["POST"])
bp_contact_v1.add_api_route("/batch", contactRouter.bulkCreate, methods=["POST"])
bp_contact_v1.add_api_route("/", contactRouter.get, methods=["GET"])
bp_contact_v1.add_api_route("/", contactRouter.update, methods=["PUT"])
bp_contact_v1.add_api_route("/{id}", contactRouter.delete, methods=["DELETE"])

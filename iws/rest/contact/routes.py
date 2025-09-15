#
# Author: Rohtash Lakra
# References:
# - https://realpython.com/flask-blueprint/
# - https://flask.palletsprojects.com/en/2.3.x/tutorial/views/#require-authentication-in-other-views
#
import logging

from flask import make_response, request

from framework.exception import DuplicateRecordException, ValidationException, RecordNotFoundException
from framework.http import HTTPStatus
from framework.orm.pydantic.model import ResponseModel
from framework.orm.sqlalchemy.schema import SchemaOperation
from rest.contact.model import Contact
from rest.contact.service import ContactService
from rest.contact.v1 import bp as bp_contact_v1

logger = logging.getLogger(__name__)


@bp_contact_v1.post("/")
def create():
    logger.debug(f"+create() => request={request}, args={request.args}, is_json:{request.is_json}")
    try:
        if request.is_json:
            body = request.get_json()
        elif request.form:
            body = request.form.to_dict()

        logger.debug(f"body={body}")
        contact = Contact(**body)
        logger.debug(f"contact={contact}")
        contactService = ContactService()
        contactService.validate(SchemaOperation.CREATE, contact)
        contact = contactService.create(contact)
        logger.debug(f"contact={contact}")

        # build success response
        response = ResponseModel(status=HTTPStatus.CREATED.statusCode, message="Contact is successfully created.")
        response.addInstance(contact)
        # response = response.to_json()
    except ValidationException as ex:
        response = ResponseModel.buildResponseWithException(ex)
    except DuplicateRecordException as ex:
        response = ResponseModel.buildResponseWithException(ex)
    except Exception as ex:
        response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

    logger.debug(f"-create() <= response={response}")
    return make_response(response.to_json(), response.status)


@bp_contact_v1.post("/batch")
def bulkCreate():
    logger.debug(f"+bulkCreate() => request={request}, args={request.args}, is_json:{request.is_json}")
    try:
        roles = []
        if request.is_json:
            body = request.get_json()
            logger.debug(f"type={type(body)}, body={body}")
            if isinstance(body, list):
                roles = [Contact(**entry) for entry in body]
            elif isinstance(body, dict):
                roles.append(Contact(**body))
            else:
                # handle form fields here.
                body = request.form.to_dict()
                roles.append(Contact(**body))

        logger.debug(f"roles={roles}")
        contactService = ContactService()
        contactService.validates(SchemaOperation.CREATE, roles)
        roles = contactService.bulkCreate(roles)
        logger.debug(f"roles={roles}")

        # build success response
        response = ResponseModel(status=HTTPStatus.CREATED.statusCode, message="Roles are successfully created.")
        response.addInstances(roles)
    except ValidationException as ex:
        response = ResponseModel.buildResponseWithException(ex)
    except DuplicateRecordException as ex:
        response = ResponseModel.buildResponseWithException(ex)
    except Exception as ex:
        response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

    logger.debug(f"-bulkCreate() <= response={response}")
    return make_response(response.to_json(), response.status)


@bp_contact_v1.get("/")
def get():
    logger.debug(f"+get() => request={request}, args={request.args}, is_json:{request.is_json}")
    try:
        contactService = ContactService()
        roles = contactService.findByFilter(request.args)

        # build success response
        response = ResponseModel.buildResponse(HTTPStatus.OK)
        if roles:
            response.addInstances(roles)
        else:
            response.message = "No Records Exist!"
    except Exception as ex:
        response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

    logger.debug(f"-get() <= response={response}")
    return make_response(response.to_json(), response.status)


@bp_contact_v1.put("/")
def update():
    logger.debug(f"+update() => request={request}, args={request.args}, is_json:{request.is_json}")
    try:
        if request.is_json:
            body = request.get_json()
            logger.debug(f"body={body}")
            contact = Contact(**body)
            logger.debug(f"contact={contact}")

        contactService = ContactService()
        contactService.validate(SchemaOperation.UPDATE, contact)
        contact = contactService.update(contact)
        logger.debug(f"contact={contact}")

        # build success response
        response = ResponseModel(status=HTTPStatus.OK.statusCode, message="Contact is successfully updated.")
        response.addInstance(contact)
    except ValidationException as ex:
        response = ResponseModel.buildResponseWithException(ex)
    except RecordNotFoundException as ex:
        response = ResponseModel.buildResponseWithException(ex)
    except Exception as ex:
        response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

    logger.debug(f"-update() <= response={response}")
    return make_response(response.to_json(), response.status)


@bp_contact_v1.delete("/<id>")
def delete(id: int):
    logger.debug(f"+delete({id}) => request={request}, args={request.args}, is_json:{request.is_json}")
    try:
        if request.is_json:
            body = request.get_json()
            logger.debug(f"body={body}")
            contact = Contact(**body)
            logger.debug(f"contact={contact}")

        contactService = ContactService()
        contactService.delete(id)
        # build success response
        response = ResponseModel(status=HTTPStatus.OK.statusCode, message="Contact is successfully deleted.")
    except RecordNotFoundException as ex:
        response = ResponseModel.buildResponseWithException(ex)
    except Exception as ex:
        response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

    logger.debug(f"-delete() <= response={response}")
    return make_response(response.to_json(), response.status)

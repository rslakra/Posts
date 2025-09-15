#
# Author: Rohtash Lakra
# References:
# - https://realpython.com/flask-blueprint/
# - https://flask.palletsprojects.com/en/2.3.x/tutorial/views/#require-authentication-in-other-views
#

import logging

from flask import make_response, request

from framework.blueprint import AbstractBlueprint
from framework.exception import DuplicateRecordException, ValidationException, NoRecordFoundException
from framework.http import HTTPStatus
from framework.orm.pydantic.model import ResponseModel
from rest.role.model import Permission
from rest.role.service import PermissionService

logger = logging.getLogger(__name__)


class PermissionBlueprint(AbstractBlueprint):
    pass


bp = PermissionBlueprint("permissions", __name__, url_prefix="/permissions")


@bp.post("/")
def create():
    logger.debug(f"+create() => request={request}, args={request.args}, is_json:{request.is_json}")
    try:
        # post_data = request.form.to_dict(flat=False)
        if request.is_json:
            body = request.get_json()
            logger.debug(f"body={body}")
            permissions = Permission(**body)
            logger.debug(f"permissions={permissions}")

        permissionService = PermissionService()
        permissions = permissionService.create(permissions)
        logger.debug(f"permissions={permissions}")
        # build success response
        response = ResponseModel(status=HTTPStatus.CREATED.statusCode, message="Permission is successfully created.")
        response.addInstance(permissions)
    except ValidationException as ex:
        response = ResponseModel.buildResponseWithException(ex)
    except DuplicateRecordException as ex:
        response = ResponseModel.buildResponseWithException(ex)
    except Exception as ex:
        response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

    logger.debug(f"-create() <= response={response}")
    return make_response(response.to_json(), response.status)


@bp.post("/batch")
def bulkCreate():
    logger.debug(f"+bulkCreate() => request={request}, args={request.args}, is_json:{request.is_json}")
    try:
        permissions = []
        if request.is_json:
            body = request.get_json()
            logger.debug(f"type={type(body)}, body={body}")
            if isinstance(body, list):
                permissions = [Permission(**entry) for entry in body]
            elif isinstance(body, dict):
                permissions.append(Permission(**body))
            else:
                # handle form fields here.
                body = request.form.to_dict()
                permissions.append(Permission(**body))

        logger.debug(f"permissions={permissions}")
        permissionService = PermissionService()
        permissions = permissionService.bulkCreate(permissions)
        logger.debug(f"permissions={permissions}")
        # build success response
        response = ResponseModel(status=HTTPStatus.CREATED.statusCode, message="Permissions are successfully created.")
        response.addInstances(permissions)
    except ValidationException as ex:
        response = ResponseModel.buildResponseWithException(ex)
    except DuplicateRecordException as ex:
        response = ResponseModel.buildResponseWithException(ex)
    except Exception as ex:
        response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

    logger.debug(f"-bulkCreate() <= response={response}")
    return make_response(response.to_json(), response.status)


@bp.get("/")
def get():
    logger.debug(f"+get() => request={request}, args={request.args}, is_json:{request.is_json}")
    try:
        permissionService = PermissionService()
        modelObjects = permissionService.findByFilter(request.args)
        # build success response
        response = ResponseModel.buildResponse(HTTPStatus.OK)
        if modelObjects:
            response.addInstances(modelObjects)
        else:
            response.message = "No Records Exist!"
    except Exception as ex:
        response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

    logger.debug(f"-get() <= response={response}")
    return make_response(response.to_json(), response.status)


@bp.put("/")
def update():
    logger.debug(f"+update() => request={request}, args={request.args}, is_json:{request.is_json}")
    try:
        if request.is_json:
            body = request.get_json()
            logger.debug(f"body={body}")
            modelObject = Permission(**body)
            logger.debug(f"modelObject={modelObject}")

        permissionService = PermissionService()
        modelObject = permissionService.update(modelObject)
        logger.debug(f"modelObject={modelObject}")

        # build success response
        response = ResponseModel(status=HTTPStatus.OK.statusCode, message="Permission is successfully updated.")
        response.addInstance(modelObject)
    except ValidationException as ex:
        response = ResponseModel.buildResponseWithException(ex)
    except NoRecordFoundException as ex:
        response = ResponseModel.buildResponseWithException(ex)
    except Exception as ex:
        response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

    logger.debug(f"-update() <= response={response}")
    return make_response(response.to_json(), response.status)


@bp.delete("/<id>")
def delete(id: int):
    logger.debug(f"+delete({id}) => request={request}, args={request.args}, is_json:{request.is_json}")
    if request.is_json:
        body = request.get_json()
        logger.debug(f"body={body}")
        modelObject = Permission(**body)
        logger.debug(f"modelObject={modelObject}")

    try:
        permissionService = PermissionService()
        permissionService.delete(id)
        # build success response
        response = ResponseModel(status=HTTPStatus.OK.statusCode, message="Permission is successfully deleted.")
    except NoRecordFoundException as ex:
        response = ResponseModel.buildResponseWithException(ex)
    except Exception as ex:
        response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

    logger.debug(f"-delete() <= response={response}")
    return make_response(response.to_json(), response.status)

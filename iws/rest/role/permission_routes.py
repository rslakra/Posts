#
# Author: Rohtash Lakra
#

import logging

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from rest.base import BaseRouter
from framework.exception import DuplicateRecordException, ValidationException, NoRecordFoundException
from framework.http import HTTPStatus
from framework.orm.pydantic.model import ResponseModel
from rest.role.model import Permission
from rest.role.service import PermissionService

logger = logging.getLogger(__name__)


bp = APIRouter(prefix="/permissions")

class PermissionRouter(BaseRouter):
    """PermissionRouter handles CRUD operations for permission resources."""

    async def create(self, request: Request):
        """Create a permission."""
        logger.debug(f"+create() => request={request}, args={request.query_params}")
        try:
            body = await self.json_or_none(request)
            permissions = None
            if body is not None:
                logger.debug(f"body={body}")
                permissions = Permission(**body)
                logger.debug(f"permissions={permissions}")

            permissionService = PermissionService()
            permissions = permissionService.create(permissions)
            logger.debug(f"permissions={permissions}")
            response = ResponseModel(status=HTTPStatus.CREATED.statusCode, message="Permission is successfully created.")
            response.addInstance(permissions)
        except ValidationException as ex:
            response = ResponseModel.buildResponseWithException(ex)
        except DuplicateRecordException as ex:
            response = ResponseModel.buildResponseWithException(ex)
        except Exception as ex:
            response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

        logger.debug(f"-create() <= response={response}")
        return JSONResponse(status_code=response.status, content=response.to_json())

    async def bulkCreate(self, request: Request):
        """Create multiple permissions in one request."""
        logger.debug(f"+bulkCreate() => request={request}, args={request.query_params}")
        try:
            permissions = []
            body = await self.json_or_none(request)
            if body is not None:
                logger.debug(f"type={type(body)}, body={body}")
                if isinstance(body, list):
                    permissions = [Permission(**entry) for entry in body]
                elif isinstance(body, dict):
                    permissions.append(Permission(**body))

            logger.debug(f"permissions={permissions}")
            permissionService = PermissionService()
            permissions = permissionService.bulkCreate(permissions)
            logger.debug(f"permissions={permissions}")
            response = ResponseModel(status=HTTPStatus.CREATED.statusCode, message="Permissions are successfully created.")
            response.addInstances(permissions)
        except ValidationException as ex:
            response = ResponseModel.buildResponseWithException(ex)
        except DuplicateRecordException as ex:
            response = ResponseModel.buildResponseWithException(ex)
        except Exception as ex:
            response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

        logger.debug(f"-bulkCreate() <= response={response}")
        return JSONResponse(status_code=response.status, content=response.to_json())

    async def get(self, request: Request):
        """Fetch permissions using optional query filters."""
        logger.debug(f"+get() => request={request}, args={request.query_params}")
        try:
            permissionService = PermissionService()
            modelObjects = permissionService.findByFilter(self.query_params(request))
            response = ResponseModel.buildResponse(HTTPStatus.OK)
            if modelObjects:
                response.addInstances(modelObjects)
            else:
                response.message = "No Records Exist!"
        except Exception as ex:
            response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

        logger.debug(f"-get() <= response={response}")
        return JSONResponse(status_code=response.status, content=response.to_json())

    async def update(self, request: Request):
        """Update an existing permission."""
        logger.debug(f"+update() => request={request}, args={request.query_params}")
        try:
            body = await self.json_or_none(request)
            modelObject = None
            if body is not None:
                logger.debug(f"body={body}")
                modelObject = Permission(**body)
                logger.debug(f"modelObject={modelObject}")

            permissionService = PermissionService()
            modelObject = permissionService.update(modelObject)
            logger.debug(f"modelObject={modelObject}")
            response = ResponseModel(status=HTTPStatus.OK.statusCode, message="Permission is successfully updated.")
            response.addInstance(modelObject)
        except ValidationException as ex:
            response = ResponseModel.buildResponseWithException(ex)
        except NoRecordFoundException as ex:
            response = ResponseModel.buildResponseWithException(ex)
        except Exception as ex:
            response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

        logger.debug(f"-update() <= response={response}")
        return JSONResponse(status_code=response.status, content=response.to_json())

    async def delete(self, id: int, request: Request):
        """Delete a permission by id."""
        logger.debug(f"+delete({id}) => request={request}, args={request.query_params}")
        try:
            body = await self.json_or_none(request)
            if body is not None:
                logger.debug(f"body={body}")
                modelObject = Permission(**body)
                logger.debug(f"modelObject={modelObject}")

            permissionService = PermissionService()
            permissionService.delete(id)
            response = ResponseModel(status=HTTPStatus.OK.statusCode, message="Permission is successfully deleted.")
        except NoRecordFoundException as ex:
            response = ResponseModel.buildResponseWithException(ex)
        except Exception as ex:
            response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

        logger.debug(f"-delete() <= response={response}")
        return JSONResponse(status_code=response.status, content=response.to_json())


permissionRouter = PermissionRouter()
bp.add_api_route("/", permissionRouter.create, methods=["POST"])
bp.add_api_route("/batch", permissionRouter.bulkCreate, methods=["POST"])
bp.add_api_route("/", permissionRouter.get, methods=["GET"])
bp.add_api_route("/", permissionRouter.update, methods=["PUT"])
bp.add_api_route("/{id}", permissionRouter.delete, methods=["DELETE"])

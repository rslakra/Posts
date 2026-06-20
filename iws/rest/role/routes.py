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
from rest.role.model import Role, RoleAssignPermission
from rest.role.service import RoleService
from rest.role.v1 import bp as bp_role_v1

logger = logging.getLogger(__name__)


class RoleRouter(BaseRouter):
    """RoleRouter encapsulates FastAPI handlers for role resources."""

    async def create(self, request: Request):
        """Create a role."""
        logger.debug(f"+create() => request={request}, args={request.query_params}")
        try:
            body = await self.json_or_none(request)
            role = None
            if body is not None:
                logger.debug(f"body={body}")
                role = Role(**body)
                logger.debug(f"role={role}")

            roleService = RoleService()
            roleService.validate(SchemaOperation.CREATE, role)
            role = roleService.create(role)
            logger.debug(f"role={role}")
            response = ResponseModel(status=HTTPStatus.CREATED.statusCode, message="Role is successfully created.")
            response.addInstance(role)
        except ValidationException as ex:
            response = ResponseModel.buildResponseWithException(ex)
        except DuplicateRecordException as ex:
            response = ResponseModel.buildResponseWithException(ex)
        except Exception as ex:
            response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

        logger.debug(f"-create() <= response={response}")
        return JSONResponse(status_code=response.status, content=response.to_json())

    async def bulkCreate(self, request: Request):
        """Create multiple roles in one request."""
        logger.debug(f"+bulkCreate() => request={request}, args={request.query_params}")
        try:
            roles = []
            body = await self.json_or_none(request)
            if body is not None:
                logger.debug(f"type={type(body)}, body={body}")
                if isinstance(body, list):
                    roles = [Role(**entry) for entry in body]
                elif isinstance(body, dict):
                    roles.append(Role(**body))

            logger.debug(f"roles={roles}")
            roleService = RoleService()
            roleService.validates(SchemaOperation.CREATE, roles)
            roles = roleService.bulkCreate(roles)
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
        """Fetch roles using optional query filters."""
        logger.debug(f"+get() => request={request}, args={request.query_params}")
        try:
            roleService = RoleService()
            roles = roleService.findByFilter(self.query_params(request))

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
        """Update an existing role."""
        logger.debug(f"+update() => request={request}, args={request.query_params}")
        try:
            body = await self.json_or_none(request)
            role = None
            if body is not None:
                logger.debug(f"body={body}")
                role = Role(**body)
                logger.debug(f"role={role}")

            roleService = RoleService()
            roleService.validate(SchemaOperation.UPDATE, role)
            role = roleService.update(role)
            logger.debug(f"role={role}")

            response = ResponseModel(status=HTTPStatus.OK.statusCode, message="Role is successfully updated.")
            response.addInstance(role)
        except ValidationException as ex:
            response = ResponseModel.buildResponseWithException(ex)
        except NoRecordFoundException as ex:
            response = ResponseModel.buildResponseWithException(ex)
        except Exception as ex:
            response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

        logger.debug(f"-update() <= response={response}")
        return JSONResponse(status_code=response.status, content=response.to_json())

    async def delete(self, id: int, request: Request):
        """Delete a role by id."""
        logger.debug(f"+delete({id}) => request={request}, args={request.query_params}")
        try:
            body = await self.json_or_none(request)
            if body is not None:
                logger.debug(f"body={body}")
                role = Role(**body)
                logger.debug(f"role={role}")

            roleService = RoleService()
            roleService.delete(id)
            response = ResponseModel(status=HTTPStatus.OK.statusCode, message="Role is successfully deleted.")
        except NoRecordFoundException as ex:
            response = ResponseModel.buildResponseWithException(ex)
        except Exception as ex:
            response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

        logger.debug(f"-delete() <= response={response}")
        return JSONResponse(status_code=response.status, content=response.to_json())

    async def assignPermission(self, request: Request):
        """Assign one or more permissions to roles."""
        logger.debug(f"+assignPermission() => request={request}, args={request.query_params}")
        try:
            rolePermissions = []
            body = await self.json_or_none(request)
            if body is not None:
                logger.debug(f"type={type(body)}, body={body}")
                if isinstance(body, list):
                    rolePermissions = [RoleAssignPermission(**entry) for entry in body]
                elif isinstance(body, dict):
                    rolePermissions.append(RoleAssignPermission(**body))

            logger.debug(f"rolePermissions={rolePermissions}")
            roleService = RoleService()
            modelObjects = roleService.assignPermissions(rolePermissions)
            logger.debug(f"modelObjects={modelObjects}")
            response = ResponseModel(status=HTTPStatus.OK.statusCode,
                                     message="Successfully granted permission to role.")
            response.addInstances(modelObjects)
        except ValidationException as ex:
            response = ResponseModel.buildResponseWithException(ex)
        except DuplicateRecordException as ex:
            response = ResponseModel.buildResponseWithException(ex)
        except Exception as ex:
            response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

        logger.debug(f"-assignPermission() <= response={response}")
        return JSONResponse(status_code=response.status, content=response.to_json())

    async def revokePermission(self, request: Request):
        """Revoke one or more permissions from roles."""
        logger.debug(f"+revokePermission() => request={request}, args={request.query_params}")
        try:
            rolePermissions = []
            body = await self.json_or_none(request)
            if body is not None:
                logger.debug(f"type={type(body)}, body={body}")
                if isinstance(body, list):
                    rolePermissions = [RoleAssignPermission(**entry) for entry in body]
                elif isinstance(body, dict):
                    rolePermissions.append(RoleAssignPermission(**body))

            logger.debug(f"rolePermissions={rolePermissions}")
            roleService = RoleService()
            modelObjects = roleService.revokePermissions(rolePermissions)
            logger.debug(f"modelObjects={modelObjects}")
            response = ResponseModel(status=HTTPStatus.OK.statusCode,
                                     message="Successfully revoked permission from role.")
            response.addInstances(modelObjects)
        except ValidationException as ex:
            response = ResponseModel.buildResponseWithException(ex)
        except DuplicateRecordException as ex:
            response = ResponseModel.buildResponseWithException(ex)
        except Exception as ex:
            response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

        logger.debug(f"-revokePermission() <= response={response}")
        return JSONResponse(status_code=response.status, content=response.to_json())


roleRouter = RoleRouter()
bp_role_v1.add_api_route("/", roleRouter.create, methods=["POST"])
bp_role_v1.add_api_route("/batch", roleRouter.bulkCreate, methods=["POST"])
bp_role_v1.add_api_route("/", roleRouter.get, methods=["GET"])
bp_role_v1.add_api_route("/", roleRouter.update, methods=["PUT"])
bp_role_v1.add_api_route("/{id}", roleRouter.delete, methods=["DELETE"])
bp_role_v1.add_api_route("/assign-permission", roleRouter.assignPermission, methods=["POST"])
bp_role_v1.add_api_route("/revoke-permission", roleRouter.revokePermission, methods=["POST"])

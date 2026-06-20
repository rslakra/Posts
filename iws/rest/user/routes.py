#
# Author: Rohtash Lakra
#
import logging

from fastapi import Request
from fastapi.responses import JSONResponse

from rest.base import BaseRouter
from framework.exception import DuplicateRecordException, ValidationException, NoRecordFoundException
from framework.http import HTTPStatus
from framework.orm.pydantic.model import ErrorModel
from framework.orm.pydantic.model import ResponseModel
from framework.orm.sqlalchemy.schema import SchemaOperation
from rest.user.model import User
from rest.user.service import UserService
from rest.user.v1 import bp as bp_account_v1

logger = logging.getLogger(__name__)


class UserRouter(BaseRouter):
    """UserRouter handles account and user management endpoints."""

    async def register(self, request: Request):
        """Register a new user."""
        logger.debug(f"+register() => request={request}, args={request.query_params}")
        try:
            body = await self.json_or_none(request)
            modelObject = None
            if body:
                if isinstance(body, list):
                    modelObject = [User(**entry) for entry in body]
                elif isinstance(body, dict):
                    modelObject = User(**body)
            else:
                raise ValidationException(httpStatus=HTTPStatus.INVALID_DATA, messages=["'User' is not fully defined!"])

            logger.debug(f"modelObject={modelObject}")
            userService = UserService()
            modelObject = userService.register(modelObject)
            response = ResponseModel(status=HTTPStatus.CREATED.statusCode, message="User is successfully created.")
            response.addInstance(modelObject)
        except ValidationException as ex:
            response = ResponseModel.buildResponseWithException(ex)
        except DuplicateRecordException as ex:
            response = ResponseModel.buildResponseWithException(ex)
        except Exception as ex:
            response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

        logger.debug(f"-register() <= response={response}")
        return JSONResponse(status_code=response.status, content=response.to_json())

    async def login(self, request: Request):
        """Authenticate a user login request."""
        logger.debug(f"+login() => request={request}, args={request.query_params}")
        body = await self.json_or_none(request)
        if body is not None:
            logger.debug(f"user={body}")

        response = ErrorModel.buildError(HTTPStatus.NOT_FOUND, "Account is not registered!")
        return JSONResponse(status_code=response.statusCode, content=response.model_dump())

    async def logout(self, request: Request):
        """Logout the current user session."""
        logger.debug(f"+logout() => request={request}, args={request.query_params}")
        return JSONResponse(status_code=200, content={"status": 200, "message": "Logged out"})

    async def forgot_password(self, request: Request):
        """Handle forgot-password request (placeholder)."""
        logger.debug(f"+forgot_password() => request={request}, args={request.query_params}")
        return JSONResponse(status_code=501, content={"status": 501, "message": "Not implemented"})

    async def bulkCreate(self, request: Request):
        """Create multiple users in one request."""
        logger.debug(f"+bulkCreate() => request={request}, args={request.query_params}")
        try:
            roles = []
            body = await self.json_or_none(request)
            if body is not None:
                logger.debug(f"type={type(body)}, body={body}")
                if isinstance(body, list):
                    roles = [User(**entry) for entry in body]
                elif isinstance(body, dict):
                    roles.append(User(**body))

            logger.debug(f"roles={roles}")
            userService = UserService()
            userService.validates(SchemaOperation.CREATE, roles)
            roles = userService.bulkCreate(roles)
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
        """Fetch users using optional query filters."""
        logger.debug(f"+get() => request={request}, args={request.query_params}")
        try:
            userService = UserService()
            roles = userService.findByFilter(self.query_params(request))
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
        """Update an existing user."""
        logger.debug(f"+update() => request={request}, args={request.query_params}")
        try:
            body = await self.json_or_none(request)
            user = User(**body) if body is not None else None
            logger.debug(f"user={user}")

            userService = UserService()
            userService.validate(SchemaOperation.UPDATE, user)
            user = userService.update(user)
            logger.debug(f"user={user}")
            response = ResponseModel(status=HTTPStatus.OK.statusCode, message="User is successfully updated.")
            response.addInstance(user)
        except ValidationException as ex:
            response = ResponseModel.buildResponseWithException(ex)
        except NoRecordFoundException as ex:
            response = ResponseModel.buildResponseWithException(ex)
        except Exception as ex:
            response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

        logger.debug(f"-update() <= response={response}")
        return JSONResponse(status_code=response.status, content=response.to_json())

    async def delete(self, id: int, request: Request):
        """Delete a user by id."""
        logger.debug(f"+delete({id}) => request={request}, args={request.query_params}")
        try:
            body = await self.json_or_none(request)
            if body is not None:
                user = User(**body)
                logger.debug(f"user={user}")

            userService = UserService()
            userService.delete(id)
            response = ResponseModel(status=HTTPStatus.OK.statusCode, message="User is successfully deleted.")
        except NoRecordFoundException as ex:
            response = ResponseModel.buildResponseWithException(ex)
        except Exception as ex:
            response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

        logger.debug(f"-delete() <= response={response}")
        return JSONResponse(status_code=response.status, content=response.to_json())


userRouter = UserRouter()
bp_account_v1.add_api_route("/register", userRouter.register, methods=["POST"])
bp_account_v1.add_api_route("/login", userRouter.login, methods=["POST"])
bp_account_v1.add_api_route("/logout", userRouter.logout, methods=["POST"])
bp_account_v1.add_api_route("/forgot-password", userRouter.forgot_password, methods=["POST"])
bp_account_v1.add_api_route("/batch", userRouter.bulkCreate, methods=["POST"])
bp_account_v1.add_api_route("/", userRouter.get, methods=["GET"])
bp_account_v1.add_api_route("/", userRouter.update, methods=["PUT"])
bp_account_v1.add_api_route("/{id}", userRouter.delete, methods=["DELETE"])

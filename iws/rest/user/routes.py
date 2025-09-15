#
# Author: Rohtash Lakra
# References:
# - https://realpython.com/flask-blueprint/
# - https://flask.palletsprojects.com/en/2.3.x/tutorial/views/#require-authentication-in-other-views
#
import logging

from flask import make_response, request
from flask import session, g

from framework.exception import DuplicateRecordException, ValidationException, RecordNotFoundException
from framework.http import HTTPStatus
from framework.orm.pydantic.model import ResponseModel
from framework.orm.sqlalchemy.schema import SchemaOperation
from rest.auth import auth
from rest.user.model import User, LoginUser
from rest.user.service import UserService
from rest.user.v1 import bp as bp_user_v1

logger = logging.getLogger(__name__)


@bp_user_v1.before_app_request
def getLoggedInUser():
    """Load LoggedIn User"""
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        # g.user = userService.find_by_id(user_id)
        g.user = None


@bp_user_v1.post("/register")
def register():
    """Register User"""
    logger.debug(
        f"+register() => request={request}, args={request.args}, is_json:{request.is_json}, form:{request.form}")
    try:
        body = None
        if request.is_json:
            body = request.get_json()
            logger.debug(f"type={type(body)}, body={body}")
        elif request.form:
            logger.debug(f"request.form={request.form}")
            # handle form fields here.
            body = request.form.to_dict()

        modelObject = None
        if body:
            # user = UserSchema(**request.get_json())
            # user = userService.register()
            # user = UserSchema.model_construct(request.get_json())
            # user = userService.create(user)
            # return user, 201
            if isinstance(body, list):
                modelObject = [User(**entry) for entry in body]
            elif isinstance(body, dict):
                modelObject = User(**body)
        else:
            raise ValidationException(httpStatus=HTTPStatus.INVALID_DATA, messages=["'User' is not fully defined!"])

        # body["birth_date"] = datetime.now().strftime("%Y-%m-%d")
        # user = User.model_validate(obj=body)
        logger.debug(f"modelObject={modelObject}")
        userService = UserService()
        modelObject = userService.register(modelObject)

        # build success response
        response = ResponseModel(status=HTTPStatus.CREATED.statusCode, message="User is successfully created.")
        response.addInstance(modelObject)
    except ValidationException as ex:
        response = ResponseModel.buildResponseWithException(ex)
    except DuplicateRecordException as ex:
        response = ResponseModel.buildResponseWithException(ex)
        # return redirect(url_for("iws.api.login"), response)
    except Exception as ex:
        response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

    # flash(error)
    logger.debug(f"-register() <= response={response}")
    return make_response(response.to_json(), response.status)


@bp_user_v1.post("/login")
def login():
    """Login User"""
    logger.debug(f"+login() => request={request}, is_json:{request.is_json}")
    try:
        body = request.get_json()
        logger.debug(f"type={type(body)}, body={body}")
        loginUser = LoginUser(**body)
        # login user
        userService = UserService()
        loginUser = userService.login(loginUser)

        # build success response
        response = ResponseModel(status=HTTPStatus.CREATED.statusCode, message="User is logged-in successfully.")
        response.addInstance(loginUser)
    except Exception as ex:
        response = ResponseModel.buildResponseWithException(ex)

    # flash(error)
    logger.debug(f"-login() <= response={response}")
    return make_response(response.to_json(), response.status)


@bp_user_v1.post("/logout")
def logout():
    """Logout User"""
    logger.debug(f"+logout() => request={request}, args={request.args}, is_json:{request.is_json}")
    # session.clear()
    try:
        # build success response
        response = ResponseModel(status=HTTPStatus.OK.statusCode, message="User is logged-out successfully.")
    except Exception as ex:
        response = ResponseModel.buildResponseWithException(ex)

    logger.debug(f"-logout() <= response={response}")
    return make_response(response.to_json(), response.status)


@bp_user_v1.post("/forgot-password")
def forgotPassword():
    """Forgot User's Password"""
    logger.debug(f"+forgotPassword() => request={request}, args={request.args}, is_json:{request.is_json}")
    try:
        # build success response
        response = ResponseModel(status=HTTPStatus.OK.statusCode, message="Forgot password link sent successfully.")
    except Exception as ex:
        response = ResponseModel.buildResponseWithException(ex)

    logger.debug(f"-forgotPassword() <= response={response}")
    return make_response(response.to_json(), response.status)


@bp_user_v1.post("/batch")
def bulkCreate():
    """Create/Register Bulk Users"""
    logger.debug(f"+bulkCreate() => request={request}, args={request.args}, is_json:{request.is_json}")
    try:
        roles = []
        if request.is_json:
            body = request.get_json()
            logger.debug(f"type={type(body)}, body={body}")
            if isinstance(body, list):
                roles = [User(**entry) for entry in body]
            elif isinstance(body, dict):
                roles.append(User(**body))
            else:
                # handle form fields here.
                pass

        logger.debug(f"roles={roles}")
        userService = UserService()
        userService.validates(SchemaOperation.CREATE, roles)
        roles = userService.bulkCreate(roles)
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


@bp_user_v1.get("/")
@auth
def findByFilter():
    """Find User's by Filter"""
    logger.debug(f"+findByFilter) => request={request}, args={request.args}, is_json:{request.is_json}")
    try:
        userService = UserService()
        userObjects = userService.findByFilter(request.args)

        # build success response
        response = ResponseModel.buildResponse(HTTPStatus.OK)
        if userObjects:
            response.addInstances(userObjects)
        else:
            response.message = "No Records Exist!"
    except Exception as ex:
        response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

    logger.debug(f"-findByFilter() <= response={response}")
    return make_response(response.to_json(), response.status)


@bp_user_v1.put("/")
def update():
    """Update User"""
    logger.debug(f"+update() => request={request}, args={request.args}, is_json:{request.is_json}")
    if request.is_json:
        body = request.get_json()
        logger.debug(f"body={body}")
        user = User(**body)
        logger.debug(f"user={user}")

    try:
        userService = UserService()
        userService.validate(SchemaOperation.UPDATE, user)
        user = userService.update(user)
        logger.debug(f"user={user}")

        # build success response
        response = ResponseModel(status=HTTPStatus.OK.statusCode, message="User is successfully updated.")
        response.addInstance(user)
    except ValidationException as ex:
        response = ResponseModel.buildResponseWithException(ex)
    except RecordNotFoundException as ex:
        response = ResponseModel.buildResponseWithException(ex)
    except Exception as ex:
        response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

    logger.debug(f"-update() <= response={response}")
    return make_response(response.to_json(), response.status)


@bp_user_v1.delete("/<id>")
def delete(id: int):
    """Delete a User"""
    logger.debug(f"+delete({id}) => request={request}, args={request.args}, is_json:{request.is_json}")
    if request.is_json:
        body = request.get_json()
        logger.debug(f"body={body}")
        user = User(**body)
        logger.debug(f"user={user}")

    try:
        userService = UserService()
        userService.delete(id)

        # build success response
        response = ResponseModel(status=HTTPStatus.OK.statusCode, message="User is successfully deleted.")
    except RecordNotFoundException as ex:
        response = ResponseModel.buildResponseWithException(ex)
    except Exception as ex:
        response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

    logger.debug(f"-delete() <= response={response}")
    return make_response(response.to_json(), response.status)

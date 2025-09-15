import functools
import logging

from flask import request, make_response, Response

from framework.exception import AuthenticationException
from framework.http import HTTPStatus
from framework.orm.pydantic.model import ResponseModel
from framework.security.jwt import TokenTypeEnum
from rest.user.service import UserService

logger = logging.getLogger(__name__)


def authErrorResponse(message: str = None) -> Response:
    logger.error(f'httpStatus={HTTPStatus.UNAUTHORIZED}, message={message}')
    authException = AuthenticationException(HTTPStatus.UNAUTHORIZED, messages=[message])
    response = ResponseModel.buildResponseWithException(authException)
    return make_response(response.to_json(), response.status)


# TODO- validate token expiry
def auth(func_name=None, role=None):
    assert callable(func_name) or func_name is None

    def _decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            bearer_token = request.headers.get('Authorization', None)
            # validate request contains bearer token
            if not bearer_token:
                return authErrorResponse('Missing Bearer Token in the request!')

            # validate the token is valid
            try:
                auth_token = parse_bearer_token(bearer_token)
            except ValueError as ex:
                return authErrorResponse("Invalid Token!")

            userService = UserService()
            userObject = userService.authenticate(TokenTypeEnum.AUTH, auth_token)
            logger.debug(f"userObject={userObject}")
            if userObject and userObject.isAuthenticated():
                logger.debug(f"AUTH userObject={userObject}")
                return func(*args, **kwargs)

            # if reaches here, always throw an error
            return authErrorResponse(HTTPStatus.UNAUTHORIZED.name)

        return wrapper

    return _decorator(func_name) if callable(func_name) else _decorator


def parse_bearer_token(auth_header):
    """
    Parses the bearer token from an Authorization header.
    
    Parameters:
    auth_header (str): The Authorization header from which to parse the token.

    Returns:
    str: The parsed bearer token.

    Raises:
    ValueError: If the auth_header is malformed or doesn't start with "Bearer ".
    """

    if not auth_header:
        raise ValueError('The auth_header is empty.')

    # A properly formed Bearer token header starts with "Bearer "
    if not auth_header.startswith('Bearer '):
        raise ValueError("Malformed 'auth_header'. It should start with 'Bearer '.")

    # Extract the token from the header
    token = auth_header[7:]

    if not token:
        raise ValueError('No Bearer token found in the auth_header.')

    return token

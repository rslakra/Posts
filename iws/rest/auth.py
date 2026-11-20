#
# Author: Rohtash Lakra
#
import logging

from fastapi import Request

from framework.exception.auth import AuthenticationException
from framework.http import HTTPStatus
from framework.security.jwt import TokenType
from rest.user.service import UserService

logger = logging.getLogger(__name__)


# TODO- validate token expiry
async def authenticate(request: Request):
    """FastAPI dependency that authenticates the bearer token of the request and returns the authenticated user.

    Usage:
        @router.get("/protected", dependencies=[Depends(authenticate)])
        @router.get("/me")
        async def me(user=Depends(authenticate)): ...

    Raises:
        AuthenticationException: (rendered as 401 by the application's exception handler) if the token is missing,
        malformed or doesn't belong to an authenticated user.
    """
    bearer_token = request.headers.get('Authorization', None)
    # validate request contains bearer token
    if not bearer_token:
        raise AuthenticationException(HTTPStatus.UNAUTHORIZED, messages=['Missing Bearer Token in the request!'])

    # validate the token is valid
    try:
        auth_token = parse_bearer_token(bearer_token)
    except ValueError:
        raise AuthenticationException(HTTPStatus.UNAUTHORIZED, messages=['Invalid Token!'])

    userService = UserService()
    userObject = userService.authenticate(TokenType.AUTH, auth_token)
    logger.debug(f"userObject={userObject}")
    if userObject and userObject.isAuthenticated():
        return userObject

    # if reaches here, always throw an error
    raise AuthenticationException(HTTPStatus.UNAUTHORIZED, messages=[HTTPStatus.UNAUTHORIZED.name])


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

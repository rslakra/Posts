from framework.exception.abstract import AbstractException


class AuthenticationException(AbstractException):
    """ Authentication Exception """
    # Raised when user identity cannot be verified.
    pass



class AuthorizationException(AbstractException):
    """ Authorization Exception """
    # Raised when identity is known but does not have required access.
    pass

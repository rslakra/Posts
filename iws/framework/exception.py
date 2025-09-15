#
# Author: Rohtash Lakra
#
import logging
from typing import List, Optional

from framework.http import HTTPStatus

logger = logging.getLogger(__name__)


class AbstractException(Exception):
    """ AbstractException class is the base for all non-exit exceptions. """

    def __init__(self, httpStatus: HTTPStatus, messages: List[Optional[str]] = None, **kwargs):
        # def __init__(self, httpStatus: HTTPStatus, messages: List[Optional[str]] = None):
        # logger.debug(f"+__init__ => type={type(self)},  httpStatus={httpStatus}, messages={messages}, kwargs={kwargs}")
        self.httpStatus = httpStatus
        self.messages = messages
        super().__init__(kwargs)
        # logger.debug(f"-__init__ ()")

    @classmethod
    def __new__(cls, *args, **kwargs):
        # logger.debug(f"+__new__ => type={type(cls)},  args={args}, kwargs={kwargs}")
        instance = super(AbstractException, cls).__new__(cls)
        # logger.debug(f"instance => type={type(instance)}")
        # instance.__init__(*args, **kwargs)

        # logger.debug(f"-__new__ returning <==  {instance}")
        return instance

    # @property
    # def httpStatus(self):
    #     return self.httpStatus
    #
    # @property
    # def messages(self):
    #     return self.messages

    # def __str__(self) -> str:
    #     """Returns the string representation of this object"""
    #     return f"{self.getClassName()} <httpStatus={self.httpStatus!r}, messages={self.messages!r}>"
    #
    # def __repr__(self) -> str:
    #     """Returns the string representation of this object"""
    #     return str(self)


class AuthenticationException(AbstractException):
    """ Authentication Exception """
    pass


class AuthorizationException(AbstractException):
    """ Authorization Exception """
    pass


class DuplicateRecordException(AbstractException):
    """ Duplicate Record Exception """

    # @staticmethod  # known case of __new__
    # def __new__(*args, **kwargs):  # real signature unknown
    #     """ Create and return a new object.  See help(type) for accurate signature. """
    #     return DuplicateRecordException("Record already exists!")

    # def __init__(self, *args, **kwargs):
    #     super().__init__(args, kwargs)
    #     logger.debug(f"args={args}, kwargs={kwargs}")
    #
    # @classmethod
    # def __new__(cls, *args, **kws):
    #     instance = super(DuplicateRecordException, cls).__new__(cls)
    #     instance.__init__(*args, **kws)
    #     return instance


class NoRecordFoundException(AbstractException):
    """ Duplicate Record exception """

    # def __init__(self, message):
    #     # Call the base class constructor with the parameters it needs
    #     super().__init__(message)
    #
    # @staticmethod  # known case of __new__
    # def __new__(*args, **kwargs):  # real signature unknown
    #     """ Create and return a new object.  See help(type) for accurate signature. """
    #     return NoRecordFoundException("Record doesn't exist!")


class ValidationException(AbstractException):
    """ Record Validation Exception """

    # def __init__(self, httpStatus: HTTPStatus, errors: List[Optional[str]] = None):
    #     super().__init__()
    #     self.httpStatus = httpStatus
    #     self.errors = errors
    #
    # @classmethod
    # def __new__(cls, *args, **kws):
    #     instance = super(ValidationException, cls).__new__(cls)
    #     instance.__init__(*args, **kws)
    #     return instance

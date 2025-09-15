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
        super().__init__(messages, kwargs)
        # logger.debug(f"-__init__ ()")
    
    @classmethod
    def __new__(cls, *args, **kwargs):
        # logger.debug(f"+__new__ => type={type(cls)},  args={args}, kwargs={kwargs}")
        instance = super(AbstractException, cls).__new__(cls, args)
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


class BadRequestException(AbstractException):
    """ Record Validation Exception """
    
    def __init__(self, messages: List[Optional[str]] = None, **kwargs):
        super().__init__(httpStatus=HTTPStatus.BAD_REQUEST, messages=messages, kwargs=kwargs)


class AuthenticationException(AbstractException):
    """ Authentication Exception """
    
    def __init__(self, messages: List[Optional[str]] = None, **kwargs):
        super().__init__(httpStatus=HTTPStatus.UNAUTHORIZED, messages=messages, kwargs=kwargs)


class AuthorizationException(AbstractException):
    """ Authorization Exception """
    
    def __init__(self, messages: List[Optional[str]] = None, **kwargs):
        super().__init__(httpStatus=HTTPStatus.UNAUTHORIZED, messages=messages, kwargs=kwargs)


class RecordNotFoundException(AbstractException):
    """ No Record Found Exception """
    
    def __init__(self, messages: List[Optional[str]] = None, **kwargs):
        super().__init__(httpStatus=HTTPStatus.NOT_FOUND, messages=messages, kwargs=kwargs)
    
    # def __init__(self, *args, **kwargs):
    #     # Call the base class constructor with the parameters it needs
    #     super().__init__(args, kwargs)
    
    # @staticmethod  # known case of __new__
    # def __new__(*args, **kwargs):  # real signature unknown
    #     """ Create and return a new object.  See help(type) for accurate signature. """
    #     return RecordNotFoundException("Record doesn't exist!")


class DuplicateRecordException(AbstractException):
    """ Duplicate Record Exception """
    
    def __init__(self, messages: List[Optional[str]] = None, **kwargs):
        super().__init__(httpStatus=HTTPStatus.CONFLICT, messages=messages, kwargs=kwargs)
    
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


class ValidationException(AbstractException):
    """ Record Validation Exception """
    
    def __init__(self, messages: List[Optional[str]] = None, **kwargs):
        super().__init__(httpStatus=HTTPStatus.INVALID_DATA, messages=messages, kwargs=kwargs)


class TooManyRequestsException(AbstractException):
    """ Record Validation Exception """
    
    def __init__(self, messages: List[Optional[str]] = None, **kwargs):
        super().__init__(httpStatus=HTTPStatus.TOO_MANY_REQUESTS, messages=messages, kwargs=kwargs)


class ServerException(AbstractException):
    """ Record Validation Exception """
    
    def __init__(self, messages: List[Optional[str]] = None, **kwargs):
        super().__init__(httpStatus=HTTPStatus.INTERNAL_SERVER_ERROR, messages=messages, kwargs=kwargs)

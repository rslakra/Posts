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



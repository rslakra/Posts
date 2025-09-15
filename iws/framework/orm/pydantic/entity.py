#
# Author: Rohtash Lakra
# Reference(s):
#  - https://docs.pydantic.dev/latest/
#

"""
Abstract and reusable entities
"""
import json

from framework.json import AbstractJSONHandler


class GetClassAttr(type):
    """GetClassAttr returns the attribute of an object"""

    def __getitem__(cls, item):
        return getattr(cls, item)


# @dataclass
class AbstractEntity(AbstractJSONHandler):
    """AbstractEntity is the base entity of all other classes"""

    # __metaclass__ = GetClassAttr

    @staticmethod
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    # def __getitem__(self, item):
    #     return self.__class__[item]

    def getClassName(self) -> str:
        """Returns the name of the class."""
        return type(self).__name__

    def json(self):
        """Serialize this object as a JSON formatted stream to fp"""
        return self.default(self)

    @classmethod
    def from_json(cls, json_input):
        if isinstance(json_input, str):
            json_dict = json.loads(json_input)
            return cls(**json_dict)
        else:
            return cls(**json_input)

    def __str__(self):
        """Returns the string representation of this object."""
        return self.getClassName()

    def __repr__(self):
        """Returns the string representation of this object."""
        return str(self)


# @dataclass
class BaseEntity(AbstractEntity):
    """BaseEntity is the base entity of all other classes"""

    @staticmethod
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, id: int = None):
        super().__init__()
        self.id = id

    def get_id(self):
        """Get ID"""
        return self.id

    def __str__(self):
        """Returns the string representation of this object."""
        return f"{self.getClassName()} <id={self.get_id()}>"

    def __repr__(self):
        """Returns the string representation of this object."""
        return str(self)


# @dataclass
class NamedEntity(BaseEntity):
    """NamedEntity used an entity with name in it"""

    @staticmethod
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, id: int = None, name: str = None):
        super().__init__(id)
        self.name = name

    def __str__(self):
        """Returns the string representation of this object."""
        return f"{self.getClassName()} <id={self.get_id()}, name={self.name}>"

    def __repr__(self):
        """Returns the string representation of this object."""
        return str(self)


# Error Entity
# @dataclass
class ErrorEntity(AbstractEntity):
    """ErrorEntity represents the error object"""

    @staticmethod
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, status, message: str, exception: Exception = None):
        super().__init__()
        self.status = status
        self.message = message
        self.exception = exception

    def __str__(self):
        """Returns the string representation of this object."""
        return f"{self.getClassName()} <status={self.status}, message={self.message}, exception={self.exception}>"
        # return f"{type(self)} <status={self.status}, message={self.message}>"

    def __repr__(self):
        """Returns the string representation of this object."""
        return str(self)


class ErrorResponse(AbstractEntity):
    """ErrorResponse represents error message"""

    @staticmethod
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, status, message: str = None, is_critical: bool = False, debug=None, exception: Exception = None):
        super().__init__()
        # current_app.logger.error('Headers:{}, Body:{}'.format(request.headers, request.get_data()))
        # current_app.logger.error('Message: {}'.format(message))

        if is_critical:
            if exception is not None:
                if debug is None:
                    debug = {}

                debug['exception'] = exception

            # current_app.logger.critical(
            #     message,
            #     exc_info=True,
            #     extra={'debug': debug} if debug is not None else {}
            # )

        self.error = ErrorEntity(status, message if message is not None else str(exception), exception)

    def __str__(self):
        """Returns the string representation of this object."""
        return f"{self.getClassName()} <error={self.error}>"

    def __repr__(self):
        """Returns the string representation of this object."""
        return str(self)

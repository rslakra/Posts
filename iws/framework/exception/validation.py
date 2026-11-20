from framework.exception.abstract import AbstractException


class ValidationException(AbstractException):
    """ Record Validation Exception """

    # Raised when request payload or domain data fails validation checks.

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

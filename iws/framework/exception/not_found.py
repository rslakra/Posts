from framework.exception.abstract import AbstractException


class RecordNotFoundException(AbstractException):
    """ Record-not-found exception """

    # Raised when lookup/update/delete expects an existing record but none is found.

    # def __init__(self, message):
    #     # Call the base class constructor with the parameters it needs
    #     super().__init__(message)
    #
    # @staticmethod  # known case of __new__
    # def __new__(*args, **kwargs):  # real signature unknown
    #     """ Create and return a new object.  See help(type) for accurate signature. """
    #     return NoRecordFoundException("Record doesn't exist!")


# Backward-compatible alias used by existing services/routes.
NoRecordFoundException = RecordNotFoundException

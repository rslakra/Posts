from framework.exception.abstract import AbstractException


class DuplicateRecordException(AbstractException):
    """ Duplicate Record Exception """

    # Raised when an insert/create action conflicts with an existing record.

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

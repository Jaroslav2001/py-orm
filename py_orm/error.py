from pydantic import ValidationError


class PyORMError(Exception):
    pass


class NotSupportDriverError(PyORMError):
    pass


class NotLinkTableModel(PyORMError):
    pass


class CastingError(PyORMError, ValidationError):
    pass

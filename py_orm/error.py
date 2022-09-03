class PyORMError(Exception):
    pass


class NotSupportDriverError(PyORMError):
    pass


class NotLinkTableModel(PyORMError):
    pass


class BinaryOperationError(PyORMError):
    pass


class ColumnError(PyORMError):
    pass

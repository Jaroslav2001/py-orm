from typing import Generic, TypeVar, Union
from .sql_builder import SQLBuilder

_T = TypeVar('_T')


class T(SQLBuilder, Generic[_T]):
    name: Union[str, int]

    def __init__(self, name: Union[str, int, None] = None):
        if name is None:
            name = ''
        self.name = name

    def __sql__(self) -> str:
        return self._decorator_template()

    def _decorator_template(self) -> str:
        return f"{{{self.name}}}"

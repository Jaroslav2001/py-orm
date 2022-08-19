from typing import Union, Optional
from .sql_builder import SQLBuilder
from .column import Column


class T(SQLBuilder):
    left: Union[str, int, Column, 'T']
    right: Union[str, int, Column, 'T', None]

    def __init__(
            self,
            name: Union[str, int, None] = None,
            *,
            c: Optional[str] = None,
    ):
        if not(c is None):
            name = Column(c)
        if name is None:
            name = ''
        self.left = name
        self.right = None

    def __eq__(self, other: 'T'):
        return self._binary_op('==', other)

    def __ne__(self, other: 'T'):
        return self._binary_op('!=', other)

    def __lt__(self, other: 'T'):
        return self._binary_op('<', other)

    def __le__(self, other: 'T'):
        return self._binary_op('<=', other)

    def __gt__(self, other: 'T'):
        return self._binary_op('>', other)

    def __ge__(self, other: 'T'):
        return self._binary_op('>=', other)

    def __sql__(self):
        return f"WHERE " \
               f"{self._decorator_template(self.left)} " \
               f"{self.comparison}" \
               f" {self._decorator_template(self.right)}"

    def _binary_op(self, __comparison: str, other: 'T'):
        self.comparison = __comparison
        self.right = self._is_value(other)
        return self

    @classmethod
    def _decorator_template(cls, value: Union[str, int, Column, 'T']) -> str:
        if isinstance(value, Column):
            return f"{value.__sql__()}"
        if isinstance(value, cls):
            return value.__sql__()
        return f"{{{value}}}"

    @staticmethod
    def _is_value(__value: 'T') -> Union[str, int, Column, 'T']:
        if __value.right is None:
            return __value.left
        return __value

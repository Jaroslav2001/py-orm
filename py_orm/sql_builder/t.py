from typing import Union, Optional, Any
from .sql_builder import SQLBuilder
from .column import Column
from .template import Template
from .value import Value
from .operator import Operator


class T(SQLBuilder):
    left: Optional['T']
    value: Union[Column, Template, Value, Operator]
    right: Optional['T']
    max_right: 'T'

    def __init__(
            self,
            name: Optional[str] = None,
            *,
            c: Optional[str] = None,
            v: Optional[Any] = None,
            t: Optional[str] = None,
    ):
        if not(c is None):
            name = Column(c)
        elif not(v is None):
            name = Value(v)
        elif not(t is None):
            name = Operator(t)

        elif name is None:
            name = ''
        if isinstance(name, str):
            name = Template(name)
        self.value = name

        self.left = None
        self.right = None

        self.max_right = self

    def __eq__(self, other: 'T') -> 'T':
        return self.add_t(T(t='=='), other)

    def __ne__(self, other: 'T') -> 'T':
        return self.add_t(T(t='!='), other)

    def __lt__(self, other: 'T') -> 'T':
        return self.add_t(T(t='<'), other)

    def __le__(self, other: 'T') -> 'T':
        return self.add_t(T(t='<='), other)

    def __gt__(self, other: 'T') -> 'T':
        return self.add_t(T(t='>'), other)

    def __ge__(self, other: 'T') -> 'T':
        return self.add_t(T(t='>='), other)

    def and_(self, other: 'T') -> 'T':
        return self.add_t(T(t='AND'), other)

    def or_(self, other: 'T') -> 'T':
        return self.add_t(T(t='OR'), other)

    def not_(self, other: 'T') -> 'T':
        return self.add_t(T(t='NOT'), other)

    def add_t(self, *args: 'T') -> 'T':
        for __right in args:
            self._link_t(self.max_right, __right)
            while not(__right.right is None):
                __right = __right.right
            self.max_right = __right
        return self

    def _link_t(self, __left: 'T', __right: 'T') -> 'T':
        __right.left = __left
        __left.right = __right
        return self

    def __sql__(self) -> str:
        if self.right is None:
            return self.value()
        else:
            return f"{self.value()} {self.right.__sql__()}"


NULL = T(t='NULL')
NOT_NULL = T(t='NOT_NULL')
NOT = T(t='NOT')


def add_(__left: 'T', __right: 'T') -> 'T':
    return __left.and_(__right)


def or_(__left: 'T', __right: 'T') -> 'T':
    return __left.or_(__right)


def not_(__value: 'T') -> 'T':
    return NOT.add_t(__value)

from abc import ABC
from typing import (
    Optional,
    Callable,
    Any,
    TypeVar,
    Sequence,
    Union,
    Type,
    overload,
    Generic,
    Tuple,
)

from .sql import SQL

from py_orm.models import TBaseModel


def node_wrapper(func: Callable[['TNode', Any], 'TNode']):
    def wrapper(cls: 'TNode', other: Any):
        if not isinstance(other, (Column, ValueWrapper, Parameter, ParameterFor, Operator)):
            other = ValueWrapper(other)
        return func(cls, other)
    return wrapper


class BaseNode(SQL, ABC):
    pass


class Node(BaseNode, ABC):
    left: Optional['TNode']
    right: Optional['TNode']

    def __init__(
            self,
            __left: Optional['TNode'] = None,
            __right: Optional['TNode'] = None,
    ):
        self.left = __left
        self.right = __right

    @node_wrapper
    def __eq__(self, other) -> 'TNode':
        return Operator('=', self, other)

    @node_wrapper
    def __ne__(self, other) -> 'TNode':
        return Operator('<>', self, other)

    @node_wrapper
    def __lt__(self, other) -> 'TNode':
        return Operator('<', self, other)

    @node_wrapper
    def __le__(self, other) -> 'TNode':
        return Operator('<=', self, other)

    @node_wrapper
    def __gt__(self, other) -> 'TNode':
        return Operator('>', self, other)

    @node_wrapper
    def __ge__(self, other) -> 'TNode':
        return Operator('>=', self, other)

    @node_wrapper
    def __add__(self, other) -> 'TNode':
        return Operator('+', self, other)

    @node_wrapper
    def __sub__(self, other) -> 'TNode':
        return Operator('-', self, other)

    @node_wrapper
    def __mul__(self, other) -> 'TNode':
        return Operator('*', self, other)

    @node_wrapper
    def __truediv__(self, other) -> 'TNode':
        return Operator('/', self, other)

    @node_wrapper
    def __and__(self, other) -> 'TNode':
        return Operator('AND', self, other)

    @node_wrapper
    def __or__(self, other) -> 'TNode':
        return Operator('OR', self, other)


class TupleNode(BaseNode):
    args: Tuple['TNode', ...]

    def __init__(self, *args):
        self.args = args

    @property
    def __sql__(self) -> str:
        return ' '.join(map(
            lambda x: x.__sql__,
            self.args
        ))


class Column(Generic[TBaseModel], Node):
    table: TBaseModel
    column: str
    alias: Optional[str]
    distinct: bool

    def __init__(
            self,
            __column: str,
            __table: Optional[TBaseModel] = None,
            *,
            alias: Optional[str] = None,
            distinct: bool = False,
    ):
        super().__init__()
        self.table = __table
        self.column = __column
        self.alias = alias
        self.distinct = distinct

    @property
    def __sql__(self) -> str:
        return f'{self.__sql__distinct}' \
               f'{self.__sql__column}'

    @property
    def __sql__distinct(self) -> str:
        if self.distinct:
            return 'DISTINCT '
        return ''

    @property
    def __sql__column(self) -> str:
        if self.alias is None:
            return f'"{self.__sql__table}{self.column}"'
        return f'"{self.__sql__table}{self.column}" AS "{self.alias}"'

    @property
    def __sql__table(self) -> str:
        if self.table is None:
            return ''
        return f"{self.table.__tabel_model__.__tabel_name__}."


C = Column


class ValueWrapper(Node):
    value: Any

    def __init__(self, __value: Any):
        super().__init__()
        self.value = __value

    @staticmethod
    def replace(_value: str) -> str:
        return _value.replace("'", "''")

    @property
    def __sql__(self) -> str:
        if isinstance(self.value, (int, float,)):
            return str(self.value)
        if isinstance(self.value, str):
            return f"'{self.replace(self.value)}'"
        if self.value is None:
            return 'NULL'


V = ValueWrapper


class ParameterBase(Node, ABC):
    value: Sequence[Union[None, int, str, Type['TBaseModel']]]

    @overload
    def __init__(self):
        ...

    @overload
    def __init__(self, args: Union[int, str, Type['TBaseModel']]):
        ...

    @overload
    def __init__(self, *args: Union[None, int, str]):
        ...

    def __init__(self, *args: Union[int, str, Type['TBaseModel']]):
        super().__init__()
        self.value = args

    @staticmethod
    def _braces(__value: Union[None, int, str] = ""):
        if __value is None:
            __value = ''
        return f"{{{__value}}}"

    def _braces_model(self, __value: Type['TBaseModel']):
        __table_name = __value.__tabel_model__.__tabel_name__
        return ", ".join(map(
            lambda x: self._braces(f"{x}"),
            __value.__fields__.keys(),
        ))


class Parameter(ParameterBase):
    @property
    def __sql__(self) -> str:
        if len(self.value) == 0:
            return self._braces()
        if len(self.value) == 1:
            if isinstance(self.value[0], (int, str,)):
                return self._braces(self.value[0])
            return self._braces_model(self.value[0])
        return ", ".join(map(self._braces, self.value))


P = Parameter


class ParameterFor(Parameter):
    @property
    def __sql__(self) -> str:
        return f"$for({super().__sql__})"


class Operator(Node):
    value: str

    def __init__(
            self,
            __value: str,
            __left: Optional['TNode'] = None,
            __right: Optional['TNode'] = None,
    ):
        super().__init__(
            __left,
            __right,
        )
        self.value = __value

    @property
    def __sql__(self) -> str:
        return f"{'' if self.left is None else self.left.__sql__+' '}" \
               f"{self.value}" \
               f"{'' if self.right is None else ' '+self.right.__sql__}"


NOT = Operator('NOT')
IN = Operator('IN')
BETWEEN = Operator('BETWEEN')
LIKE = Operator('LIKE')
GLOB = Operator('GLOB')
IS = Operator('IS')
ALL = Operator('ALL')


TNode = TypeVar('TNode', bound=BaseNode)

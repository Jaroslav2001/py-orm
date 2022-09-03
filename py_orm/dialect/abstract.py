from abc import ABC, abstractmethod
from typing import (
    Union,
    Tuple,
    TypeVar,
    Optional,
    Any,
)

from typing_extensions import (
    Type,
    overload,
)


class DialectAbstract(ABC):
    @classmethod
    @overload
    def type_sql(cls, type_: Type[int], value: Optional[int] = None) -> str:
        ...

    @classmethod
    @overload
    def type_sql(cls, type_: Type[float], value: Optional[int] = None) -> str:
        ...

    @classmethod
    @overload
    def type_sql(cls, type_: Type[str], value: Optional[int] = None) -> str:
        ...

    @classmethod
    @overload
    def type_sql(cls, type_: Type[bytes], value: Optional[int] = None) -> str:
        ...

    @classmethod
    @overload
    def type_sql(cls, type_: Type[bool], value: None = None) -> str:
        ...

    @classmethod
    @abstractmethod
    def type_sql(
            cls,
            type_: Type,
            value: Union[int, Tuple[int, int], None] = None
    ) -> str:
        ...

    @staticmethod
    @abstractmethod
    def py_sql(value: Any) -> str:
        ...

    @staticmethod
    @abstractmethod
    def sql_py(value: str) -> Any:
        ...


TDialectAbstract = TypeVar('TDialectAbstract', bound=DialectAbstract)

from typing import (
    Any,
    Union,
    Tuple,
)

from typing_extensions import (
    Type,
)

from .abstract import DialectAbstract


class Sqlite(DialectAbstract):
    @classmethod
    def type_sql(cls, type_: Type, value: Union[int, Tuple[int, int], None] = None) -> str:
        if isinstance(type_, int):
            return f"INTEGER{cls.type_sql_value(value)}"
        if isinstance(type_, float):
            return f"REAL{cls.type_sql_value(value)}"
        if isinstance(type_, str):
            return f"TEXT{cls.type_sql_value(value)}"
        if isinstance(type_, bytes):
            return f"BLOB{cls.type_sql_value(value)}"
        if isinstance(type_, bool):
            return f"INTEGER(1)"

    @staticmethod
    def type_sql_value(value: Union[int, Tuple[int, int], None]):
        if value is None:
            return ''
        if isinstance(value, int):
            return f"({value})"
        return f"({value[0]}, {value[1]})"

    @staticmethod
    def py_sql(value: Any) -> str:
        pass

    @staticmethod
    def sql_py(value: str) -> Any:
        pass

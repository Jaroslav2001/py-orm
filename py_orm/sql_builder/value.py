from typing import Any

from sql_builder.sql_builder import SQLBuilder


class Value(SQLBuilder):
    _value: Any

    def __init__(
            self,
            __value: Any,
    ):
        self._value = __value

    def __sql__(self) -> str:
        return self.decorator_value(self._value)

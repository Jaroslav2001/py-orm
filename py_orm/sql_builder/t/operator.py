from ..sql_builder import SQLBuilder


class Operator(SQLBuilder):
    _value: str

    def __init__(self, __value):
        self._value = __value

    def __sql__(self) -> str:
        return self._value

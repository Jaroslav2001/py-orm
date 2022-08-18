from typing import Any

from .sql_builder import SQLBuilder


class C(SQLBuilder):
    column: str
    comparison: str
    value: Any

    def __init__(
            self,
            column: str
    ):
        self.column = column

    def __eq__(self, other):
        self.comparison = '=='
        self.value = self.decorator_value(other)
        return self

    def __ne__(self, other):
        self.comparison = '!='
        self.value = self.decorator_value(other)
        return self

    def __lt__(self, other):
        self.comparison = '<'
        self.value = self.decorator_value(other)
        return self

    def __le__(self, other):
        self.comparison = '<='
        self.value = self.decorator_value(other)
        return self

    def __gt__(self, other):
        self.comparison = '>'
        self.value = self.decorator_value(other)
        return self

    def __ge__(self, other):
        self.comparison = '>='
        self.value = self.decorator_value(other)
        return self

    def __str__(self):
        return f"WHERE {self.column} {self.comparison} {self.value}"

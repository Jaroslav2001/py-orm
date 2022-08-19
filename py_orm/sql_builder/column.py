from .sql_builder import SQLBuilder
from .template import T


class C(SQLBuilder):
    column: str
    comparison: str
    value: T

    def __init__(
            self,
            column: str
    ):
        self.column = column

    def __eq__(self, other: T):
        self.comparison = '=='
        self.value = other
        return self

    def __ne__(self, other: T):
        self.comparison = '!='
        self.value = other
        return self

    def __lt__(self, other: T):
        self.comparison = '<'
        self.value = other
        return self

    def __le__(self, other: T):
        self.comparison = '<='
        self.value = other
        return self

    def __gt__(self, other: T):
        self.comparison = '>'
        self.value = other
        return self

    def __ge__(self, other: T):
        self.comparison = '>='
        self.value = other
        return self

    def __sql__(self):
        return f"WHERE {self.column} {self.comparison} {self.value()}"

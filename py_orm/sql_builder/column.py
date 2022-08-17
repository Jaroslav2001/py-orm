from typing import Any


class C:
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
        self.value = other
        return self

    def __ne__(self, other):
        self.comparison = '!='
        self.value = other
        return self

    def __lt__(self, other):
        self.comparison = '<'
        self.value = other
        return self

    def __le__(self, other):
        self.comparison = '<='
        self.value = other
        return self

    def __gt__(self, other):
        self.comparison = '>'
        self.value = other
        return self

    def __ge__(self, other):
        self.comparison = '>='
        self.value = other
        return self

    def __str__(self):
        return f"WHERE {self.column} {self.comparison} {self.value}"

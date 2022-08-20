from typing import Union, Tuple, Set
from ..sql_builder import SQLBuilder


class Template(SQLBuilder):
    name: str

    def __init__(
            self,
            name: Union[str, int, None] = None,
    ):
        if name is None:
            name = ''
        self.name = name

    def __sql__(self) -> str:
        return f"{{{self.name}}}"

from typing import Union, Tuple

from ..sql_builder import SQLBuilder


from .attribute import Attribute


class Column(SQLBuilder):
    name: str
    type_: str
    length: Union[int, Tuple[int, int], None]
    attribute: Attribute

    def __init__(
            self,
            name: str,
            type_: str,
            length: Union[int, Tuple[int, int], None],
            attribute: Attribute,
    ):
        self.name = name
        self.type_ = type_
        self.length = length
        self.attribute = attribute

    def __sql__(self) -> str:
        return f"{self.name} {self.type_} {self.attribute.__sql__()}"

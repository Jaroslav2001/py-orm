from typing import Union, Tuple

from pydantic import BaseModel as _BaseModel


from attribute import Attribute


class Column(_BaseModel):
    name: str
    type_: str
    length: Union[int, Tuple[int, int], None] = None
    attribute: Attribute

    def __sql__(self) -> str:
        return f"{self.name} {self.type_} {self.attribute.__sql__()}"

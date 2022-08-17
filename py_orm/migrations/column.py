from typing import Type, Union, Tuple

from pydantic import BaseModel

from attribute import Attribute


class Column(BaseModel):
    name: str
    type_: str
    length: Union[int, Tuple[int, int], None] = None
    attribute: Attribute

from typing import Type

from pydantic import BaseModel

from attribute import Attribute


class Column(BaseModel):
    name: str
    type_: Type
    attribute: Attribute

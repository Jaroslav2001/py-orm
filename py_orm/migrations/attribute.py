from typing import Union, Tuple

from pydantic import BaseModel


class Attribute(BaseModel):
    length: Union[int, Tuple[int, int], None]
    primary_key: bool
    foreign_key: bool
    unique: bool
    index: bool
    auto_increment: bool

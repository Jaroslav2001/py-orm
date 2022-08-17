from typing import Dict, Literal, Union

from .abstract import DialectSQL
from .sqlite import sqlite

dialect: Dict[Union[str, Literal['sqlite']], DialectSQL] = {
    'sqlite': sqlite,
}


def add_dialect(**kwargs: DialectSQL):
    global dialect
    dialect += kwargs

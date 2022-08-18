from typing import Dict, Literal, Union, TYPE_CHECKING, TypeAlias

from .abstract import DialectSQL
from .sqlite import sqlite

if TYPE_CHECKING:
    from py_orm.driver.init import Driver

DialectType: TypeAlias = Literal['sqlite', 'mysql', 'postgresql']

dialect: Dict[DialectType, DialectSQL] = {
    'sqlite': sqlite,
}

default_driver: Dict[DialectType, 'Driver'] = {
    'sqlite': 'sqlite3',
    'mysql': 'pymysql',
    'postgresql': 'psycopg2',
}

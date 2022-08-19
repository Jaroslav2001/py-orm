from typing import (
    Dict,
    Any,
    Tuple,
    TYPE_CHECKING,
    TypeAlias,
    Literal,
)

from .abstract import DialectSQL
from .sqlite import sqlite

if TYPE_CHECKING:
    from py_orm.driver.init import Driver

DialectType: TypeAlias = Literal['sqlite', 'mysql', 'postgresql']

dialect: Dict[DialectType, DialectSQL] = {
    'sqlite': sqlite,
}

default_driver: Dict[Tuple[DialectType, bool], 'Driver'] = {
    ('sqlite', False): 'sqlite3',
    ('mysql', False): 'pymysql',
    ('postgresql', False): 'psycopg2',
    ('sqlite', True): 'aiosqlite',
    ('mysql', True): 'aiomysql',
    ('postgresql', True): 'asyncpg',
}


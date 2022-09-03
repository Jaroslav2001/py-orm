from typing import (
    List,
)

from typing_extensions import (
    Literal,
    TypeAlias,
)


Driver: TypeAlias = Literal[
    "asyncpg", "aiomysql", "aiosqlite",
]
drivers: List[Driver] = [
    "asyncpg", "aiomysql", "aiosqlite",
]

from typing import (
    Literal,
    TypeAlias,
    List
)

Driver: TypeAlias = Literal[
    "asyncpg", "aiomysql", "aiosqlite",
]
drivers: List[Driver] = [
    "asyncpg", "aiomysql", "aiosqlite",
]

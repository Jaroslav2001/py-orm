from typing import (
    TYPE_CHECKING,
    TypedDict,
    Tuple,
    Union,
    Any,
    Literal,
)

if TYPE_CHECKING:
    from .driver.sync import TConnection, TCursor


class ConfigDict(TypedDict):
    """Global config PY ORM"""
    driver: Tuple[Union['TConnection', Any], Union['TCursor', Any]]
    connect: Tuple[list, dict]
    dialect: Union[str, Literal['sqlite', 'mysql', 'postgresql']]
    migrate_dir: str
    async_: bool

from typing import (
    TYPE_CHECKING,
    TypedDict,
    Tuple,
    Union,
    Any,
)

if TYPE_CHECKING:
    from .driver.sync import TConnection, TCursor


class ConfigDict(TypedDict):
    """Global config PY ORM"""
    driver: Tuple[Union['TConnection', Any], Union['TCursor', Any]]
    connect: Tuple[list, dict]
    migrate_dir: str

from typing import (
    TYPE_CHECKING,
    Tuple,
    Union,
    Literal,
    Optional,
    Type,
)

from pydantic import BaseModel

if TYPE_CHECKING:
    from .driver.sync import TConnection, TCursor
    from .driver.async_ import (
        TConnection as TConnectionAsync,
        TCursor as TCursorAsync,
    )


class Config(BaseModel):
    url: str
    migrate_dir: str


class ConfigFull(Config):
    # auto config
    driver: Tuple[
        Union[Type['TConnection'], Type['TConnectionAsync'], Type],
        Union[Type['TCursor'], Type['TCursorAsync'], Type]
    ]
    dialect: Literal['sqlite', 'mysql', 'postgresql']
    async_: bool

    username: Optional[str]
    password: Optional[str]
    host: Optional[str]
    port: Optional[int]
    database: str

from typing import (
    Literal,
    Optional,
)

from pydantic import BaseModel

from py_orm.driver.init import Driver


class Config(BaseModel):
    url: str
    migrate_dir: str


class ConfigFull(Config):
    # auto config
    driver: Driver
    dialect: Literal['sqlite', 'mysql', 'postgresql']
    async_: bool

    username: Optional[str]
    password: Optional[str]
    host: Optional[str]
    port: Optional[int]
    database: str

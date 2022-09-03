import re
from typing import (
    Optional,
)

from typing_extensions import (
    Literal,
    NoReturn,
)

from pydantic import BaseModel

from py_orm.dialect.main import DialectType
from py_orm.driver.init import Driver


class Config(BaseModel):
    url: str
    migrate_dir: str


class ConfigFull(Config):
    # auto config
    driver: Optional[Driver]
    dialect: Literal['sqlite', 'mysql', 'postgresql']

    username: Optional[str]
    password: Optional[str]
    host: Optional[str]
    port: Optional[int]
    database: str


def set_config(config: Config) -> NoReturn:
    driver_name_: Optional[Driver]
    connect = re.search(
        r"^(\w*)\+?(\w*):\/\/(.*)$",
        config.url
    ).groups()
    dialect: DialectType = connect[0]
    if connect[1] == '':
        driver_name_ = None
    else:
        driver_name_ = connect[1]
    connect = connect[2]

    if dialect in ("sqlite",):
        username = None
        password = None
        host = None
        port = None
        database = connect
    else:
        connect = re.search(
            r'^(\w*):(\w*)@(\w*):(\w*)\/(\w*)$',
            connect
        ).groups()
        username = connect[0]
        password = connect[1]
        host = connect[2]
        port = int(connect[3])
        database = connect[4]

    BaseModel.__config_py_orm__ = ConfigFull(
        url=config.url,
        migrate_dir=config.migrate_dir,
        driver=driver_name_,
        dialect=dialect,
        username=username,
        password=password,
        host=host,
        port=port,
        database=database,
    )

    BaseModel

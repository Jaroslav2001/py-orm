from typing import Type
from py_orm import BaseModel
from .abstract import AbstractConnector


def get_db() -> Type[AbstractConnector]:
    if "aiosqlite" == BaseModel.__config_py_orm__.driver:
        from .aiosqlite import Connection
        return Connection

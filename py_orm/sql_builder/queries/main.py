from typing import Set, TypeVar

from typing_extensions import TYPE_CHECKING

import pydantic
from pydantic import BaseModel as _BaseModel

if TYPE_CHECKING:
    from py_orm.config import ConfigFull
    from py_orm.driver.abstract import TAbstractConnector


class ModelMetaclass(pydantic.main.ModelMetaclass):
    __py_orm__: Set['TBaseModel'] = set()
    if TYPE_CHECKING:
        __config_py_orm__: ConfigFull
        __connector__: TAbstractConnector

    def __new__(mcs, name, bases, namespace, **kwargs):
        return super().__new__(
            mcs,
            name,
            bases,
            namespace,
            **kwargs,
        )


class BaseModel(_BaseModel, metaclass=ModelMetaclass):
    __py_orm__: Set['TBaseModel']
    __config_py_orm__: 'ConfigFull'
    __connector__: 'TAbstractConnector'


TBaseModel = TypeVar('TBaseModel', bound=BaseModel)

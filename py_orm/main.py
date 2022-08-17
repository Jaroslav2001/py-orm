from typing import (
    Set,
    TypeVar,
    Optional,
    Union,
    Any,
    Literal,
    Tuple,
    NoReturn,
    Type,
)

from pydantic import (
    BaseModel as _BaseModel,
)
import pydantic.main

from setting import ConfigDict


def is_type(_type: Any, type_name: Literal[
    'Optional', 'Union'
]) -> Tuple[bool, Tuple[Type, ...], Type]:
    """Check annotations example <'List' (int,)>"""
    if hasattr(_type, '_name'):
        if getattr(_type, '_name') == type_name:
            return True, getattr(_type, '__args__'), getattr(_type, '_name')
        return False, getattr(_type, '__args__'), getattr(_type, '_name')
    return False, tuple(), _type


class ModelMetaclass(pydantic.main.ModelMetaclass):
    __py_orm__: Set['TBaseModel'] = set()
    __config_py_orm__: ConfigDict

    def __new__(mcs, name, bases, namespace, **kwargs):
        _base_model: _BaseModel = super().__new__(
            mcs,
            name,
            bases,
            namespace,
            **kwargs,
        )

        if hasattr(namespace, '__tabel_name__'):
            _name_table = getattr(namespace, '__tabel_name__')
            if isinstance(_name_table, bool):
                if _name_table:
                    setattr(_base_model, '__tabel_name__', name)
                    mcs.__py_orm__.add(_base_model)
            if isinstance(_name_table, str):
                setattr(_base_model, '__tabel_name__', name)
                mcs.__py_orm__.add(_base_model)

        return _base_model


class BaseModel(_BaseModel, metaclass=ModelMetaclass):
    __py_orm__: Set['TBaseModel']
    __tabel_name__: Optional[Union[bool, str]]


def set_config(config: ConfigDict) -> NoReturn:
    BaseModel.__config_py_orm__ = config


TBaseModel = TypeVar('TBaseModel', bound=BaseModel)

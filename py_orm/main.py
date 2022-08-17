from typing import (
    Set,
    TypeVar,
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

        if '__tabel_name__' in namespace:
            _name_table = namespace.get('__tabel_name__')
            if isinstance(_name_table, bool):
                if _name_table:
                    namespace['__tabel_name__'] = name

        _base_model: _BaseModel = super().__new__(
            mcs,
            name,
            bases,
            namespace,
            **kwargs,
        )

        if hasattr(_base_model, '__tabel_name__'):
            if isinstance(getattr(_base_model, '__tabel_name__'), str):
                mcs.__py_orm__.add(_base_model)
            if isinstance(getattr(_base_model, '__tabel_name__'), bool):
                if getattr(_base_model, '__tabel_name__'):
                    mcs.__py_orm__.add(_base_model)

        return _base_model


class BaseModel(_BaseModel, metaclass=ModelMetaclass):
    __py_orm__: Set['TBaseModel']
    __tabel_name__: Union[bool, str]


def set_config(config: ConfigDict) -> NoReturn:
    BaseModel.__config_py_orm__ = config


TBaseModel = TypeVar('TBaseModel', bound=BaseModel)

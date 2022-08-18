import re
from typing import (
    Set,
    TypeVar,
    Union,
    Any,
    Literal,
    Tuple,
    NoReturn,
    Type,
    Optional,
)

from pydantic import (
    BaseModel as _BaseModel,
)
import pydantic.main

from setting import Config, ConfigFull
from dialect.main import default_driver, DialectType


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
    __config_py_orm__: ConfigFull

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
                _base_model.__tabel_model__ = _base_model
                mcs.__py_orm__.add(_base_model)
            if isinstance(getattr(_base_model, '__tabel_name__'), bool):
                if getattr(_base_model, '__tabel_name__'):
                    _base_model.__tabel_model__ = _base_model
                    mcs.__py_orm__.add(_base_model)

        return _base_model


class BaseModel(_BaseModel, metaclass=ModelMetaclass):
    __py_orm__: Set['TBaseModel']
    __tabel_name__: Union[bool, str]
    __tabel_model__: Optional['TBaseModel']


def set_config(config: Config) -> NoReturn:
    from py_orm.driver.init import get_driver, is_async, Driver
    driver_name_: Driver
    connect = re.search(
        r"^(\w*)\+?(\w*):\/\/(.*)$",
        config.url
    ).groups()
    dialect: DialectType = connect[0]
    if connect[1] == '':
        driver_name_ = default_driver[dialect]
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
        driver=get_driver(driver_name_),
        dialect=dialect,
        async_=is_async(driver_name_),
        username=username,
        password=password,
        host=host,
        port=port,
        database=database,
    )


TBaseModel = TypeVar('TBaseModel', bound=BaseModel)

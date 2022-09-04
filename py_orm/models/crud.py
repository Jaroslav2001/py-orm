from typing import (
    TypeVar,
)

from typing_extensions import (
    Type,
    TYPE_CHECKING,
)

from .main import ModelMetaclass, BaseModel

if TYPE_CHECKING:
    from .db import TBaseModelDB


class ModelMetaclassCRUD(ModelMetaclass):
    def __new__(mcs, name, bases, namespace, **kwargs):
        _base_model: Type[TBaseModelCRUD] = super().__new__(
            mcs,
            name,
            bases,
            namespace,
            **kwargs,
        )
        return _base_model


class BaseModelCRUD(BaseModel, metaclass=ModelMetaclassCRUD):
    __tabel_model__: 'TBaseModelDB'


TBaseModelCRUD = TypeVar('TBaseModelCRUD', bound=BaseModelCRUD)

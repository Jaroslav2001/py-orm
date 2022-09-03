from typing import Optional, Union, Tuple, Any, Type, TYPE_CHECKING

from py_orm import BaseModel, Field

if TYPE_CHECKING:
    from .model import ModelDB
    from .migrate import MigrateDB


class ConvertColumn(BaseModel):
    name: str
    type_: Type
    length: Union[int, Tuple[int, int], None]
    unique: bool
    not_null: bool
    default: Any


class ColumnDB(BaseModel):
    __tabel_name__ = 'py_orm_column'
    id: Optional[int] = Field(..., primary_key=True, auto_increment=True)

    migrate: Union[None, int, 'MigrateDB'] = Field(..., foreign_key='id')
    model: Union[None, id, 'ModelDB'] = Field(..., foreign_key='id')

    name: str
    type_: str
    length: Optional[str]
    unique: bool
    not_null: bool
    default: str

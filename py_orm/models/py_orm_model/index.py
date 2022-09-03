from typing import Optional, TYPE_CHECKING

from py_orm import BaseModel, Field

if TYPE_CHECKING:
    from .model import ModelDB
    from .column import ColumnDB


class IndexDB(BaseModel):
    __tabel_name__ = 'py_orm_index'
    id: Optional[int] = Field(..., primary_key=True, auto_increment=True)
    name: str
    model: 'ModelDB'
    column: 'ColumnDB'

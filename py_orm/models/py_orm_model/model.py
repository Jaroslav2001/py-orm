from typing import Optional, TYPE_CHECKING, Union

from py_orm import BaseModel, Field


if TYPE_CHECKING:
    from .migrate import MigrateDB


class ModelDB(BaseModel):
    __tabel_name__ = 'py_orm_model'
    id: Optional[int] = Field(..., primary_key=True, auto_increment=True)

    migrate: Union[None, int, 'MigrateDB'] = Field(..., foreign_key='id')

    name: str
    class_name: str

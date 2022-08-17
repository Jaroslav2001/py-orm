from typing import Optional

from pydantic import BaseModel as _BaseModel

from py_orm import BaseModel
from py_orm.dialect import dialect


class Attribute(_BaseModel):
    primary_key: bool = False
    foreign_key: Optional[str] = None
    unique: bool = False
    index: bool = False
    auto_increment: bool = False
    null: bool = True

    def __sql__(self) -> str:
        _dialect = dialect[BaseModel.__config_py_orm__['dialect']]
        _content = []
        if self.primary_key:
            _content.append(_dialect['primary_key'])
        if self.unique:
            _content.append(_dialect['unique'])
        if self.index:
            _content.append(_dialect['index'])
        if self.auto_increment:
            _content.append(_dialect['auto_increment'])
        if not self.null:
            _content.append(_dialect['not_null'])
        return ' '.join(_content)

from typing import Optional

from py_orm import BaseModel, Field


class MigrateDB(BaseModel):
    __tabel_name__ = 'py_orm_migrate'
    id: Optional[int] = Field(..., primary_key=True, auto_increment=True)
    commit: str
    migrate_sql: str
    rollback_sql: str

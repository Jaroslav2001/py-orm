from typing import List

from pydantic import BaseModel

from migrations.column import Column


class MigrationsModel(BaseModel):
    name: str
    columns: List[Column]

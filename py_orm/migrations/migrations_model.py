from typing import Tuple

from pydantic import BaseModel

from migrations.column import Column


class MigrationsModel(BaseModel):
    name: str
    columns: Tuple[Column]

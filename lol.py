from sqlite3 import Connection, Cursor
from py_orm import BaseModel, Field, set_config, py_orm_app


set_config(
    config={
        'connect': (['lol.db'], {}),
        'driver': (Connection, Cursor),
        'dialect': 'sqlite',
        'migrate_dir': 'lol_mi',
    }
)


class User(BaseModel):
    __tabel_name__ = True
    id: int = Field(primary_key=True, auto_increment=True)
    name: str


if __name__ == '__main__':
    print(BaseModel.__py_orm__)
    py_orm_app()

from sqlite3 import Connection, Cursor
from typing import Optional

from py_orm import BaseModel, Field, Create, py_orm_app, set_config, Read, C

set_config(
    config={
        'connect': (['lol.db'], {}),
        'driver': (Connection, Cursor),
        'dialect': 'sqlite',
        'migrate_dir': 'lol',
        'async_': False,
    }
)


class UserBase(BaseModel):
    name: str


class UserDB(UserBase):
    __tabel_name__ = 'user'
    id: Optional[int] = Field(primary_key=True, auto_increment=True)


class UserCreate(UserBase):
    __tabel_model__ = UserDB


class User(UserBase):
    __tabel_model__ = UserDB
    id: int = Field(primary_key=True, auto_increment=True)


py_orm_app()


from py_orm.driver.sync import connect
connect_ = connect()
cursor = connect_.cursor()
cursor.execute(
    Create(UserCreate).value(UserCreate(name='Lol'))
)
print(Create(UserCreate).value(UserCreate(name='Lol')))
print(Read(User).where(C('id') == 1))
print(list(
    cursor.get_all(
        Read(User).where(C('id') == 1)
    )
))
connect_.commit()

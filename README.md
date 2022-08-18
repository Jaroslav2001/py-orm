# PY ORM

---
**Documentation:** [https://jaroslav2001.github.io/py-orm](https://jaroslav2001.github.io/py-orm)

**Source Code:** [https://github.com/Jaroslav2001/py-orm](https://github.com/Jaroslav2001/py-orm)

---

## ORM based on pydantic model

```python title="example code" linenums="1"
from sqlite3 import Connection, Cursor
from typing import Optional

from py_orm import set_config, BaseModel, Field, py_orm_app, Create, Read, C

set_config(
    config={
        'connect': (['data.db'], {}),
        'driver': (Connection, Cursor),
        'dialect': 'sqlite',
        'migrate_dir': 'migrate',
        'async_': False,
    }
)


class UserBase(BaseModel):
    name: str


class UserDB(UserBase):
    __tabel_name__ = 'user'
    id: Optional[int] = Field(..., primary_key=True, auto_increment=True)


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int


py_orm_app()

if __name__ == '__main__':
    from py_orm.driver.sync import connect
    connect_ = connect()
    cursor = connect_.cursor()
    cursor.execute(
        Create(UserDB, UserCreate).value(UserCreate(name='Lol'))
    )
    print(Create(UserDB, UserCreate).value(UserCreate(name='Lol')))
    print(Read(UserDB, User).where(C('id') == 1))
    print(list(
        cursor.get_all(
            Read(UserDB, User).where(C('id') == 1)
        )
    ))
    connect_.commit()

```
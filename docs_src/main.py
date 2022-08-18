from typing import Optional

from py_orm import (
    BaseModel,
    Field,
    Create,
    py_orm_app,
    set_config,
    Read,
    C,
    Config,
)

set_config(
    Config(
        url='sqlite://lol.db',
        migrate_dir='lol',
    )
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


def main():
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


if __name__ == '__main__':
    main()

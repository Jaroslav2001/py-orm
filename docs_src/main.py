from typing import Optional

from py_orm import (
    BaseModel,
    Field,
    Create,
    py_orm_app,
    set_config,
    Read,
    C,
    T,
    Config,
)

set_config(
    Config(
        url='sqlite://data.db',
        migrate_dir='data',
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
    create = Create(UserCreate)
    cursor.exec_create(
        create,
        UserCreate(name='Hello')
    )
    print(create)

    read_only: Read[User] = Read(User).where(C('id') == T('id'))
    print(read_only())
    print(read_only)
    cursor.exec_read(read_only, id=1)
    print(list(
        cursor.get_all(
            User
        )
    ))
    read: Read[User] = Read(User).where(C('name') == T())
    print(read())
    cursor.exec_read(read, 'Hello')
    print(list(
        cursor.get_all(
            User
        )
    ))
    connect_.commit()


if __name__ == '__main__':
    main()


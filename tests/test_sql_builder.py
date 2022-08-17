from py_orm import BaseModel, InsertInto, Field


def test_insert_into():
    class UserBase(BaseModel):
        name: str

    class User(UserBase):
        __tabel_name__ = True
        id: str = Field(primary_key=True, auto_increment=True)

    class UserCreate(UserBase):
        pass

    a = InsertInto[UserBase, UserCreate](UserBase, UserCreate).values(UserCreate(name='lol')).__sql__()
    print(a)

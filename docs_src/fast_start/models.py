from typing import Optional
from py_orm import BaseModel, Field


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

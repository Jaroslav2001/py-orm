from typing import Optional, TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from pydantic.fields import ModelField

from py_orm import __version__, BaseModel, Field
from py_orm.main import ModelMetaclass


def test_version():
    assert __version__ == '0.1.0'


def test_base_orm():
    assert type(BaseModel) == ModelMetaclass


def test_create_class():
    class User(BaseModel):
        id: Optional[int] = Field(None, primary_key=True)
        name: str

    class Phone(BaseModel):
        id: Optional[int] = Field(None, primary_key=True)
        number: str
        user: None

    a = User(name='Lol')

    x: Dict[str, 'ModelField'] = User.__fields__
    b = getattr(User.__annotations__['id'], '__args__')
    c = User.__annotations__['id']._name

    assert User == User

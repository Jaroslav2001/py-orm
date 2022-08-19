from py_orm import Create, Read, T
from models import User, UserCreate

from py_orm.driver.sync import connect

# create connect and cursor
connect_ = connect()
cursor = connect_.cursor()

# create new entry
cursor.create(
    Create(UserCreate),
    UserCreate(name='Hello')
)
connect_.commit()

# read entry
print(list(
    cursor.read_all(
        Read(User).where(T(c='name') == T()),
        'Hello'
    )
))
connect_.commit()

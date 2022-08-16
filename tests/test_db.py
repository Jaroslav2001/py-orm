import sqlite3
from py_orm import set_config
from py_orm.driver.sync import connect, TCursor


def test_db():
    set_config(
        config={
            'driver': (sqlite3.Connection, sqlite3.Cursor),
            'connect': ([':memory:'], {}),
            'migrate_dir': '',
        }
    )
    a = connect()
    c: TCursor = a.cursor()
    assert a == c.connection

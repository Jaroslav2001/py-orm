from sqlite3 import Connection, Cursor
from py_orm import set_config


def test_config():
    set_config(
        config={
            'connect': ([], {}),
            'driver': (Connection, Cursor),
            'dialect': 'sqlite',
            'migrate_dir': 'migrate',
        }
    )

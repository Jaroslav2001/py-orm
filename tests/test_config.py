from sqlite3 import Connection
from py_orm import set_config


def test_config():
    set_config(
        config={
            'driver': Connection,
            'url': ([], {}),
            'migrate_files': '',
        }
    )

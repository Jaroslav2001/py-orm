import sqlite3

from typer.testing import CliRunner

from py_orm import set_config, py_orm_app


def test_db():
    set_config(
        config={
            'driver': (sqlite3.Connection, sqlite3.Cursor),
            'connect': ([':memory:'], {}),
            'dialect': 'sqlite',
            'migrate_dir': '',
        }
    )
    if "__main__" == __name__:
        runner = CliRunner()
        runner.invoke(py_orm_app, [])
    from py_orm.driver.sync import connect, TCursor
    a = connect()
    c: TCursor = a.cursor()
    assert a == c.connection

import sqlite3

from typer.testing import CliRunner

from py_orm import set_config, py_orm_app, BaseModel, Field, validator


def test_schema_db():
    pass


def test_create_migrate():
    set_config(
        config={
            'driver': (sqlite3.Connection, sqlite3.Cursor),
            'dialect': 'sqlite',
            'connect': ([':memory:'], {}),
            'migrate_dir': 'migrations',
        }
    )

    class User(BaseModel):
        id: int = Field(..., primary_key=True)
        name: str

    if "__main__" == __name__:
        runner = CliRunner()
        runner.invoke(py_orm_app, ['migrate', 'create'])
    from py_orm.driver.sync import connect, TCursor
    a = connect()
    c: TCursor = a.cursor()
    assert a == c.connection

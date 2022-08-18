import sys
from typer import Typer

from . import info
from . import migrate


app = Typer()


app.add_typer(info.app, name='info')
app.add_typer(migrate.app, name='migrate')


def py_orm_app():
    if len(sys.argv) > 1:
        app()


if __name__ == '__main__':
    py_orm_app()

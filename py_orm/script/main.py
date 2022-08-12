from typer import Typer

from . import info
from . import migrate


app = Typer()


app.add_typer(info.app, name='info')
app.add_typer(migrate.app, name='migrate')


if __name__ == '__main__':
    app()

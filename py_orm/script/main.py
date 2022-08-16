from typer import Typer

from . import info
from . import migrate


app = Typer()


app.add_typer(info.app, name=info.__name__)
app.add_typer(migrate.app, name=migrate.__name__)


if __name__ == '__main__':
    app()

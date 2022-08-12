from typer import Typer, echo
from py_orm import __version__


app = Typer()


@app.command()
def version():
    echo(f'py_orm: {__version__}')

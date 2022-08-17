from typer import Typer

from . import info
from . import migrate


app = Typer()


app.add_typer(info.app, name='info')
app.add_typer(migrate.app, name='migrate')


@app.callback(invoke_without_command=True)
def callback():
    pass


if __name__ == '__main__':
    app()

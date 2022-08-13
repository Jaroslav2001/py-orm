from typer import Typer, echo
import py_orm


app = Typer()


@app.command()
def version():
    echo(f'{py_orm.__name__}: {py_orm.__version__}')

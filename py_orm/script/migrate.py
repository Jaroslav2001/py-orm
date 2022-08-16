from os import mkdir
from os.path import join

from typer import Typer


app = Typer()


@app.command()
def init():
    pass


@app.command()
def create():
    pass


@app.command()
def run():
    pass

from typer import Typer

from py_orm.migrations import *


app = Typer()


@app.command()
def create(yes: bool = False):
    create_sql_migrate(yes=yes)


# Parsing sql migrate file
# -- *(<(?:migrate|rollback) *[0-9]+> *\n[\s\w(),]*;)
# <((?:migrate|rollback)) *([0-9]+)> *\n([\s\w(),]*;)

# --.*<start>\n([\w\s(),;-]*)--.*<end>
# --.*migrate\n([\w\s(),;-]*)--.*rollback\n([\w\s(),;-]*)

@app.command()
def run():
    migrate()


@app.command()
def rollback():
    migrate(rollback=True)

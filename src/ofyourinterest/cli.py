# mypy: ignore-errors

"""Console script for ofyourinterest."""

import typer
from rich.console import Console

from ofyourinterest import utils

app = typer.Typer()
console = Console()


@app.command()
def main():
    """Console script for ofyourinterest."""
    console.print("Replace this message by putting your code into ofyourinterest.cli.main")
    console.print("See Typer documentation at https://typer.tiangolo.com/")
    utils.do_something_useful()


if __name__ == "__main__":
    app()

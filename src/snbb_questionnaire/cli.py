"""Console script for snbb_questionnaire."""
import snbb_questionnaire

import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command()
def main():
    """Console script for snbb_questionnaire."""
    console.print("Replace this message by putting your code into "
               "snbb_questionnaire.cli.main")
    console.print("See Typer documentation at https://typer.tiangolo.com/")
    


if __name__ == "__main__":
    app()

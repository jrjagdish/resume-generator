import typer
from tracelens.cli.stats import stats_command

app = typer.Typer()
app.command("stats")(stats_command)

def run():
    app()  # type: ignore

if __name__ == "__main__":
    run()

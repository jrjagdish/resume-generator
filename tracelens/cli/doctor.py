import typer
import os
from tracelens.core.config import model as config_model
from tracelens.utils.pathways import get_current_log_file

def doctor():
    """Run diagnostics to check if TraceLens is set up correctly."""
    typer.echo("Running TraceLens diagnostics...\n")

    log_file = get_current_log_file()
    typer.echo(f"Log file path: {log_file}")

    if not log_file.parent.exists():
        typer.secho("Logs directory does not exist.", fg=typer.colors.RED)
    else:
        typer.secho("Logs directory exists.", fg=typer.colors.GREEN)

    if not log_file.exists():
        typer.secho("Log file does not exist. It will be created on first log write.", fg=typer.colors.YELLOW)
    else:
        typer.secho("Log file exists.", fg=typer.colors.GREEN)

    try:
        with log_file.open("a") as f:
            f.write("")  # Just to test write permission
        typer.secho("Log file is writable.", fg=typer.colors.GREEN)
    except Exception as e:
        typer.secho(f"Log file is not writable: {e}", fg=typer.colors.RED)

    config = config_model.TraceLensConfig.load()
    if config.enabled:
        typer.secho("TraceLens is enabled in the configuration.", fg=typer.colors.GREEN)
    else:
        typer.secho("TraceLens is disabled in the configuration.", fg=typer.colors.YELLOW)

    typer.echo("\nDiagnostics completed.")
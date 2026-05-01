import click
import subprocess
import sys
from importlib import import_module


@click.group()
def cli():
    """InstantGrade command line interface."""
    pass


@cli.command()
@click.option("--host", default="127.0.0.1", help="Host to bind the UI server to")
@click.option("--port", default=8501, help="Port for the UI server")
@click.option("--open/--no-open", default=True, help="Open browser after launch")
def launch(host, port, open):
    """Launch the Streamlit UI for InstantGrade.

    This finds the installed `instantgrade.ui.streamlit_app` file and runs
    `streamlit run <file>` so the UI opens in the browser.
    """
    try:
        mod = import_module("instantgrade.ui.streamlit_app")
        app_path = getattr(mod, "__file__", None)
        if app_path is None:
            click.echo("Could not locate streamlit app file.")
            sys.exit(1)

        cmd = [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            app_path,
            "--server.port",
            str(port),
            "--server.address",
            host,
        ]

        click.echo(f"Running: {' '.join(cmd)}")
        # Launch Streamlit in the foreground so user can see logs.
        subprocess.run(cmd)

    except Exception as e:
        click.echo(f"Failed to launch Streamlit UI: {e}")
        sys.exit(1)

import click
import socket
import subprocess
import sys
import threading
import time
import webbrowser
from importlib import import_module


@click.group()
def cli():
    """InstantGrade command line interface."""
    pass


def _is_port_available(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind((host, port))
        except OSError:
            return False
    return True


def _choose_port(host: str, preferred_port: int, attempts: int = 10) -> int | None:
    for port in range(preferred_port, preferred_port + attempts):
        if _is_port_available(host, port):
            return port
    return None


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

        resolved_port = _choose_port(host, port)
        if resolved_port is None:
            click.echo(f"No free port found in range {port}-{port + 9}.")
            sys.exit(1)

        if resolved_port != port:
            click.echo(f"Port {port} is not available. Using {resolved_port} instead.")

        url = f"http://{host}:{resolved_port}"

        cmd = [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            app_path,
            "--server.port",
            str(resolved_port),
            "--server.address",
            host,
        ]

        click.echo(f"Running: {' '.join(cmd)}")
        click.echo(f"Open: {url}")

        if open:
            threading.Thread(
                target=lambda: (time.sleep(1.5), webbrowser.open(url)),
                daemon=True,
            ).start()

        # Launch Streamlit in the foreground so user can see logs.
        completed = subprocess.run(cmd)
        if completed.returncode != 0:
            sys.exit(completed.returncode)

    except Exception as e:
        click.echo(f"Failed to launch Streamlit UI: {e}")
        sys.exit(1)

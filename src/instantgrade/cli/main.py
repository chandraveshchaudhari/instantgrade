# instantgrade/cli/main.py
"""Command-line interface for InstantGrade.

This module provides CLI commands for running evaluations from the terminal.
"""

import click
from pathlib import Path
from instantgrade import Evaluator


@click.group()
def cli():
    """InstantGrade CLI – Automated evaluation from the terminal.

    This command-line interface provides tools for evaluating student
    submissions against instructor solutions. Supports Jupyter notebooks
    and Excel files.

    Examples
    --------
    Evaluate submissions:

        $ instantgrade evaluate -s solution.ipynb -f submissions/

    Save reports to custom directory:

        $ instantgrade evaluate -s solution.ipynb -f submissions/ -o reports/
    """
    pass


@cli.command()
@click.option(
    "--solution",
    "-s",
    required=True,
    type=click.Path(exists=True, dir_okay=False),
    help="Path to instructor solution file (.ipynb or .xlsx)",
)
@click.option(
    "--submissions",
    "-f",
    required=True,
    type=click.Path(exists=True, file_okay=False),
    help="Folder containing student submissions",
)
@click.option(
    "--output", "-o", required=False, type=click.Path(), help="Optional output folder for reports"
)
def evaluate(solution, submissions, output):
    """Evaluate student submissions against a solution.

    Runs the complete evaluation pipeline: loads the solution and submissions,
    executes them, compares outputs, and generates detailed reports.

    Parameters
    ----------
    solution : str
        Path to the instructor's solution file.
    submissions : str
        Path to folder containing student submission files.
    output : str, optional
        Path to directory for saving reports. Created if it doesn't exist.

    Examples
    --------
    Basic evaluation:

        $ instantgrade evaluate -s solution.ipynb -f submissions/

    With custom output directory:

        $ instantgrade evaluate -s sol.ipynb -f subs/ -o reports/
    """

    solution = Path(solution)
    submissions = Path(submissions)

    click.echo(f"Loading evaluator...")
    evaluator = Evaluator(
        solution_file_path=str(solution),
        submission_folder_path=str(submissions),
    )

    click.echo(f"Running evaluation...")
    report = evaluator.get_report()

    click.echo("\n=== Evaluation Report ===")
    click.echo(report)

    if output:
        # optional: write report to a JSON file
        import json

        output = Path(output)
        output.mkdir(parents=True, exist_ok=True)
        out_path = output / "report.json"
        out_path.write_text(json.dumps(report, indent=2), encoding="utf8")
        click.echo(f"\nSaved report to: {out_path}")


if __name__ == "__main__":
    cli()

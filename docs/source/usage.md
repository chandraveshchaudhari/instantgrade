# Usage Guide

This page summarizes the main workflows supported by InstantGrade.

## Launching the UI

```bash
instantgrade launch
```

Optional flags:

```bash
instantgrade launch --host 127.0.0.1 --port 8501 --open
```

If the requested port is busy, InstantGrade tries the next free port automatically.

## UI workflows

The UI supports:

- one instructor `.ipynb` upload
- multiple student notebook uploads
- additional dataset and support file uploads
- ZIP uploads that are extracted automatically
- local execution mode
- Docker execution mode
- saved run history
- downloadable HTML, PDF, and log artifacts
- student notebook generation from an instructor solution

## Python notebook grading

For notebook grading, the instructor solution notebook should follow this structure:

1. A markdown cell starting with `##` introduces the question.
2. The next code cell contains the reference implementation.
3. The following code cell contains setup code and `assert` statements.

Notes:

- setup code is executed before the assertions for that question
- supporting data files can be placed with the solution or uploaded with submissions
- student notebooks should set `name` and `roll_number`

## Local vs Docker execution

### Local execution

Use local execution when:

- Docker is unavailable
- you want to use the current host Python environment
- you are iterating quickly during development

### Docker execution

Use Docker execution when:

- Docker is installed and running
- you want isolation between student code and the host
- you want more reproducible grading runs across machines

## Python API

```python
from instantgrade import InstantGrader

grader = InstantGrader(
    solution_file_path="path/to/solution.ipynb",
    submission_folder_path="path/to/submissions",
    use_docker=True,
    best_n=None,
)

report = grader.run()
summary = grader.summary()
report.to_html("reports/report.html")
```

## Excel grading

InstantGrade can also route Excel grading automatically when the solution file is an Excel workbook.

Supported formats:

- `.xlsx`
- `.xls`
- `.xlsm`

## Output artifacts

Notebook grading runs can produce:

- HTML report output
- PDF report output when PDF tooling is available
- execution logs
- per-student assertion results

## Common troubleshooting

### Docker mode fails immediately

Check that Docker is installed and the daemon is running. If not, rerun in local mode.

### Notebooks cannot find data files

Upload the required files in the UI or place them beside the solution or submission notebooks.

### Docker seems to use old code

Force a rebuild of the Docker image or rebuild it explicitly from the repository.
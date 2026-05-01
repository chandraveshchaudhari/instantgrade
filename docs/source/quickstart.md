# Quick Start

This walkthrough covers the fastest path from installation to a working grading run.

## 1. Install InstantGrade

```bash
python3 -m pip install instantgrade
```

## 2. Launch the UI

```bash
instantgrade launch
```

Open the printed URL in your browser. If `8501` is unavailable, InstantGrade automatically uses the next free port.

## 3. Prepare your grading inputs

For notebook grading, gather:

- one instructor solution notebook
- one or more student notebooks
- any supporting files required by the notebooks, such as `.csv`, `.json`, `.txt`, or spreadsheets

You can upload files directly in the UI or point to existing server paths.

## 4. Choose execution mode

- Use local mode when Docker is not installed or not running
- Use Docker mode only when Docker is installed and available

## 5. Start grading

In the UI:

- upload the instructor notebook
- upload the student notebooks
- upload any additional data files if needed
- choose local or Docker execution
- run grading

When grading finishes, the UI shows the report and saves the run to the local InstantGrade runs directory.

## 6. Review and download results

From the UI you can:

- open the generated HTML report
- download the HTML report
- download the PDF report when available
- download the execution log
- reopen earlier saved runs from run history

## 7. Generate a student notebook template

The UI can generate a student-facing notebook from an instructor solution notebook.

Use this when you want:

- function stubs instead of instructor implementations
- assertions removed from the student copy
- a quick distribution-ready notebook template

## Python API example

```python
from instantgrade import InstantGrader

grader = InstantGrader(
    solution_file_path="data/python_example/sample_solutions.ipynb",
    submission_folder_path="data/python_example/submissions",
    use_docker=False,
)

report = grader.run()
report.to_html("reports/report.html")
```
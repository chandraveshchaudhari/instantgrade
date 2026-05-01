# Examples

This page highlights a few common InstantGrade workflows.

## Example 1: Launch the grading UI

```bash
instantgrade launch
```

Use this when you want a browser-based workflow for uploads, execution, history, and downloads.

## Example 2: Grade notebooks locally

```python
from instantgrade import InstantGrader

grader = InstantGrader(
    solution_file_path="data/python_example/sample_solution_with_tests.ipynb",
    submission_folder_path="data/python_example/submissions",
    use_docker=False,
)

report = grader.run()
report.to_html("reports/python_local.html")
```

## Example 3: Grade notebooks with Docker

```python
from instantgrade import InstantGrader

grader = InstantGrader(
    solution_file_path="data/python_example/sample_solution_with_tests.ipynb",
    submission_folder_path="data/python_example/submissions",
    use_docker=True,
)

report = grader.run()
```

Use this only when Docker is installed and running.

## Example 4: Grade Excel submissions

```python
from instantgrade import InstantGrader

grader = InstantGrader(
    solution_file_path="data/excel_example/Assignment_ sol 1.xlsx",
    submission_folder_path="data/excel_example/submissions",
)
```

For spreadsheet workflows, point the solution path to the instructor workbook used by the Excel evaluator.

## Example 5: Generate a student notebook template

Launch the UI, open the student notebook generation section, upload the instructor solution notebook, and download the generated student copy.
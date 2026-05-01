# API Reference

InstantGrade exposes a small top-level routing API for most workflows.

## `InstantGrader`

`InstantGrader` selects the correct evaluator based on the input paths and delegates execution to the Python notebook evaluator or the Excel evaluator.

### Basic usage

```python
from instantgrade import InstantGrader

grader = InstantGrader(
    solution_file_path="path/to/solution.ipynb",
    submission_folder_path="path/to/submissions",
    use_docker=False,
)

report = grader.run()
```

### Key methods

- `run()` executes grading and returns the reporting object
- `to_html(path)` writes the report to an HTML file
- `summary()` returns the evaluator summary when available

## Python evaluator parameters

Common parameters for notebook grading:

- `solution_file_path`
- `submission_folder_path`
- `use_docker`
- `parallel_workers`
- `log_path`
- `log_level`
- `best_n`
- `scaled_range`

## Report output

The reporting layer provides the consolidated student results used by the UI and HTML report generation.

## Entry points

- CLI: `instantgrade launch`
- Python import: `from instantgrade import InstantGrader`
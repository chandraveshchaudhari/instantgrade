# InstantGrade Documentation

Welcome to **InstantGrade**, an automated evaluation framework for grading Python Jupyter notebooks and Excel spreadsheets. InstantGrade simplifies the assessment process by comparing student submissions against reference solutions and generating comprehensive HTML reports.

```{toctree}
:maxdepth: 2
:caption: Contents

installation
quickstart
usage
examples
api
contributing
changelog
```

## What is InstantGrade?

InstantGrade is a powerful tool designed for educators and course administrators who need to:

- ✅ **Automate grading** of Jupyter notebooks and Excel files
- 📊 **Compare outputs** between student submissions and reference solutions
- 📝 **Generate reports** showing detailed comparisons and scores
- ⚡ **Save time** by eliminating manual comparison work
- 🎯 **Ensure consistency** in grading across multiple submissions

## Key Features

### 🐍 Python Notebook Support
- Execute and compare Jupyter notebooks
- Run locally or inside Docker
- Upload supporting datasets and other files alongside notebooks
- Use instructor question context plus assertions for grading

### 📊 Excel File Support
- Compare spreadsheet data
- Support for multiple sheets
- Formula validation
- Cell-by-cell difference highlighting

### 📈 Comprehensive Reporting
- HTML reports with detailed comparisons
- Visual diff highlighting
- Score calculations
- Execution logs and error tracking

### 🖥️ Streamlit UI
- Launch with `instantgrade launch`
- Automatic fallback to the next free port when `8501` is unavailable
- Upload one instructor notebook, many student notebooks, and extra data files
- Generate a student-facing notebook from an instructor solution

### 🔧 Flexible Workflows
- Customizable evaluation criteria
- Support for multiple file formats
- Batch processing capabilities
- CLI and Python API
- Saved run history with downloadable HTML, PDF, and log artifacts

## Quick Example

```python
from instantgrade import InstantGrader

grader = InstantGrader(
    solution_file_path="solution.ipynb",
    submission_folder_path="submissions/",
    use_docker=False,
)

report = grader.run()
report.to_html("reports/report.html")

# Results are saved to an HTML report.
```

## Use Cases

### Education
- Grade programming assignments
- Evaluate data analysis projects
- Assess Excel spreadsheet exercises
- Provide detailed feedback to students

### Training
- Evaluate workshop exercises
- Check coding bootcamp submissions
- Assess certification exams

### Research
- Validate experimental results
- Compare data analysis outputs
- Reproduce computational research

## Get Started

- [Installation](installation.md)
- [Quick Start](quickstart.md)
- [Usage Guide](usage.md)
- [Examples](examples.md)
- [API Reference](api.md)
- [Contributing](contributing.md)

## Community & Support

- **GitHub**: [chandraveshchaudhari/instantgrade](https://github.com/chandraveshchaudhari/instantgrade)
- **Issues**: Report bugs or request features on [GitHub Issues](https://github.com/chandraveshchaudhari/instantgrade/issues)
- **PyPI**: [pypi.org/project/instantgrade](https://pypi.org/project/instantgrade/)

## License

InstantGrade is released under the MIT License. See the [LICENSE](https://github.com/chandraveshchaudhari/instantgrade/blob/master/LICENSE.txt) file for details.

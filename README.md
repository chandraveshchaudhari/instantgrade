<table>
   <tr>
      <td valign="middle">
   <img src="https://raw.githubusercontent.com/chandraveshchaudhari/chandraveshchaudhari/initial_setup/data/logo.png" alt="Dr. Chandravesh Chaudhari Logo" style="max-width: 100%; width: 180px; height: auto;" />
      </td>
      <td valign="middle" style="padding-left: 20px;">
         <h1 style="margin:0">InstantGrade</h1>
         <p style="margin-top:4px; margin-bottom:6px; font-size:1.05rem; color:#444">
            An automated evaluation framework for Python notebooks and Excel assignments
         </p>
      </td>
   </tr>
</table>

[![PyPI version](https://badge.fury.io/py/instantgrade.svg)](https://pypi.org/project/instantgrade/)
[![Python](https://img.shields.io/pypi/pyversions/instantgrade.svg)](https://pypi.org/project/instantgrade/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://chandraveshchaudhari.github.io/instantgrade/)
[![CI](https://github.com/chandraveshchaudhari/instantgrade/workflows/Test%20Package%20Build/badge.svg)](https://github.com/chandraveshchaudhari/instantgrade/actions)
[![codecov](https://codecov.io/gh/chandraveshchaudhari/instantgrade/branch/master/graph/badge.svg)](https://codecov.io/gh/chandraveshchaudhari/instantgrade)

---

## 🌱 Dr. Chandravesh Chaudhari

[![Website](https://img.shields.io/badge/🌐_Website-Visit-00C853?style=for-the-badge)](https://chandraveshchaudhari.github.io/website/)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/chandraveshchaudhari)
[![Email](https://img.shields.io/badge/Email-Contact-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:chandraveshchaudhari@gmail.com)

Dr. Chandravesh Chaudhari is the maintainer of InstantGrade — an automated evaluation platform currently focused on grading Python Jupyter notebooks and Excel assignments and more to follow in future.

Contact & social links:

- Email: [chandraveshchaudhari@gmail.com](mailto:chandraveshchaudhari@gmail.com)
- Website: https://chandraveshchaudhari.github.io/website/
- LinkedIn: https://www.linkedin.com/in/chandraveshchaudhari

---

## 📚 Documentation

**[Read the full documentation →](https://chandraveshchaudhari.github.io/instantgrade/)**

- **[Installation Guide](https://chandraveshchaudhari.github.io/instantgrade/installation.html)** - Get started in minutes
- **[Quick Start](https://chandraveshchaudhari.github.io/instantgrade/quickstart.html)** - Your first evaluation
- **[Usage Guide](https://chandraveshchaudhari.github.io/instantgrade/usage.html)** - Comprehensive features
- **[API Reference](https://chandraveshchaudhari.github.io/instantgrade/api.html)** - Complete API documentation
- **[Examples](https://chandraveshchaudhari.github.io/instantgrade/examples.html)** - Real-world use cases

---

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Supported File Types](#supported-file-types)
- [Contribution](#contribution)
- [Future Improvements](#future-improvements)

## Introduction
InstantGrade is a comprehensive, extensible evaluation framework designed to automatically grade student submissions against instructor solution files. It supports multiple file formats including Python Jupyter notebooks and Excel files, making it ideal for educational institutions and online learning platforms.

The framework was created to streamline the grading process for programming and data analysis assignments, reducing manual effort while providing detailed, actionable feedback to students. The vision is to expand support to additional file types and programming languages, creating a universal evaluation platform for technical education. 


## 👩‍🏫 About the Maintainer

**Dr. Chandravesh Chaudhari**

📧 [chandraveshchaudhari@gmail.com](mailto:chandraveshchaudhari@gmail.com)
🌐 [Website](https://chandraveshchaudhari.github.io/website/)
🔗 [LinkedIn](https://www.linkedin.com/in/chandraveshchaudhari)


## Features
- **Launchable Web UI**: Start the Streamlit interface with `instantgrade launch` after `pip install instantgrade`
- **Smart Port Fallback**: If port `8501` is busy, the launcher automatically selects the next free port
- **Notebook Grading**: Grade Python `.ipynb` submissions against an instructor solution notebook
- **Excel Grading**: Grade Excel assignments (`.xlsx`, `.xls`, `.xlsm`) with the Excel evaluator
- **Multiple Submission Uploads**: Upload one instructor notebook and multiple student notebooks in the UI
- **Additional Data File Uploads**: Upload supporting files such as `.csv`, `.json`, `.txt`, and spreadsheet assets needed by notebooks
- **ZIP Upload Support**: Upload zipped submissions or zipped supporting files and let the UI extract them
- **Local or Docker Execution**: Use local execution when Docker is unavailable, or Docker isolation when Docker is installed and running
- **Student Notebook Generation**: Generate a student-facing notebook template from an instructor solution notebook
- **Run History and Downloads**: Review saved runs and download HTML reports, PDF reports, and execution logs
- **Comprehensive Reporting**: Generate detailed HTML reports with scoring and per-assertion feedback
- **Extensible Architecture**: Add new evaluator types without changing the main routing API

#### Significance
- **Time-Saving**: Reduces manual grading effort by 90% for programming assignments
- **Consistency**: Ensures uniform evaluation criteria across all student submissions
- **Detailed Feedback**: Provides students with specific areas of improvement
- **Scalability**: Handles large classes with hundreds of submissions efficiently
- **Educational Focus**: Allows instructors to focus on teaching rather than repetitive grading tasks

## Installation
This project is available at [PyPI](https://pypi.org/project/instantgrade/).

### Install from PyPI
```bash
python3 -m pip install instantgrade  
```

After installation you can launch the UI directly:

```bash
instantgrade launch
```

If port `8501` is already in use, InstantGrade will try the next available port automatically and print the actual URL.

### Local-only usage

You do **not** need Docker to use InstantGrade in local mode.

- Use local mode when Docker is not installed
- Use local mode when Docker Desktop or Docker Engine is installed but not running
- In the UI, choose local execution for notebook grading when you want everything to run on the host Python environment

### Docker-backed notebook grading

Docker is required only when you want isolated notebook execution.

- Install Docker Desktop on macOS or Windows: https://www.docker.com/products/docker-desktop
- Install Docker Engine on Linux: https://docs.docker.com/engine/install/
- Make sure Docker is installed and the daemon is running before using Docker mode in the UI or `use_docker=True` in Python

Verify Docker availability:

```bash
docker --version
docker info
```

If Docker is unavailable, switch to local execution instead of Docker execution.

### Development installation
```bash
git clone https://github.com/chandraveshchaudhari/instantgrade.git
cd instantgrade
python3 -m pip install -e .
```

When upgrading InstantGrade, existing local Docker images may be stale. To avoid runtime mismatches inside containers, do one of the following after upgrading:

- Prefetch a new image tagged to the current commit (recommended):

```bash
# from the repository root
python tools/docker_build_image.py

# to force a rebuild even if an image exists
python tools/docker_build_image.py --force
```

- Or allow the runtime to rebuild automatically for a single run:

```bash
instantgrade_FORCE_REBUILD=1 instantgrade launch
```

- Developer fast-iteration option: bind-mount the `src` directory into the container so you do not need to rebuild the image on small changes.

The repository ships a small helper at `tools/docker_build_image.py` that builds a git-SHA-tagged image (and also tags `instantgrade:latest` for convenience). This is the recommended step for administrators preparing a new release in their environment.

### Dependencies
##### Required
- [pandas](https://pandas.pydata.org/) - Data manipulation and analysis for comparison results
- [openpyxl](https://openpyxl.readthedocs.io/) - Reading and writing Excel files
- [nbformat](https://nbformat.readthedocs.io/) - Working with Jupyter notebook files
- [nbclient](https://nbclient.readthedocs.io/) - Executing Jupyter notebooks programmatically
- [click](https://click.palletsprojects.com/) - Creating command-line interfaces

##### Optional
- [xlwings](https://www.xlwings.org/) - Advanced Excel automation capabilities (Windows/macOS only)

## Usage

### Launch the UI

```bash
instantgrade launch
```

The UI supports these workflows:

- Upload one instructor `.ipynb` notebook
- Upload multiple student notebooks in one run
- Upload additional supporting files such as datasets and other assets
- Use local execution or Docker execution
- Generate a student notebook from the instructor solution notebook
- Review previous runs and download saved artifacts

### Python API

```python
from instantgrade import InstantGrader

# Grade notebooks locally
grader = InstantGrader(
   solution_file_path="path/to/solution.ipynb",
   submission_folder_path="path/to/submissions/",
   use_docker=False,
)

report = grader.run()
report.to_html("reports/report.html")
```

### Python API with Docker

```python
from instantgrade import InstantGrader

grader = InstantGrader(
   solution_file_path="path/to/solution.ipynb",
   submission_folder_path="path/to/submissions/",
   use_docker=True,
)

report = grader.run()
```

### Instructor notebook pattern for Python grading

For Python notebook grading, the instructor solution notebook should follow this pattern:

- A markdown cell starting with `##` defines a question
- The next code cell contains the reference function or solution code
- The following code cell contains setup code and `assert` statements used for grading

Assertions written as `assert actual == expected` produce the most useful diagnostics.

### Example commands
```bash
instantgrade launch --port 8501
```

## Supported File Types

### Python Jupyter Notebooks (.ipynb)
- Executes notebooks locally or in Docker
- Uses question setup code plus assertion-based grading
- Resolves supporting dataset files placed with the solution or submission bundle
- Produces detailed per-question pass/fail results and identity checks

### Excel Files (.xlsx, .xls, .xlsm)
- Cell value comparison across worksheets
- Formula evaluation and verification
- Conditional formatting checks
- Chart and pivot table analysis (with xlwings)

### Future Support (Planned)
- R Markdown files (.Rmd)
- Python scripts (.py)
- SQL files (.sql)
- MATLAB scripts (.m)

## Important links
- [Documentation](https://chandraveshchaudhari.github.io/instantgrade/)
- [Quick tour](https://github.com/chandraveshchaudhari/instantgrade/blob/master/data/python_example/basic_python_flow.ipynb)
- [Project maintainer (feel free to contact)](mailto:chandraveshchaudhari@gmail.com?subject=[GitHub]%20Evaluator) 
- [Future Improvements](https://github.com/chandraveshchaudhari/instantgrade/projects)
- [License](https://github.com/chandraveshchaudhari/instantgrade/blob/master/LICENSE.txt)

## Contribution
All kinds of contributions are appreciated:
- [Improving readability of documentation](https://github.com/chandraveshchaudhari/instantgrade/wiki)
- [Feature Request](https://github.com/chandraveshchaudhari/instantgrade/issues/new/choose)
- [Reporting bugs](https://github.com/chandraveshchaudhari/instantgrade/issues/new/choose)
- [Contribute code](https://github.com/chandraveshchaudhari/instantgrade/compare)
- [Asking questions in discussions](https://github.com/chandraveshchaudhari/instantgrade/discussions)

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

For detailed contribution guidelines, see the [Contributing Guide](https://chandraveshchaudhari.github.io/instantgrade/contributing.html).



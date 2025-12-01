# Development Guide for InstantGrade

## Setup Development Environment

### 1. Clone and Install

```bash
# Clone the repository
git clone https://github.com/chandraveshchaudhari/instantgrade.git
cd instantgrade

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with all dependencies
pip install -e ".[dev,docs]"
```

### 2. Install Pre-Commit Hooks (Recommended)

Pre-commit hooks automatically format and check your code before each commit:

```bash
# Install pre-commit
pip install pre-commit

# Set up the hooks
pre-commit install

# (Optional) Run on all files to check
pre-commit run --all-files
```

After this, every time you `git commit`, the hooks will:
- Format code with Black
- Check for common issues
- Trim trailing whitespace
- Validate YAML/JSON files

## Code Formatting

### Automatic Formatting

**Option 1: Use the Makefile**
```bash
# Format all code
make format

# Check formatting without changes
make check
```

**Option 2: Run Black directly**
```bash
# Format all source code
python3 -m black src/

# Check formatting (CI mode)
python3 -m black --check src/
```

### VS Code Setup

If using VS Code, the `.vscode/settings.json` file is already configured to:
- Format on save automatically
- Use Black as the formatter
- Run Flake8 linting

**Required VS Code Extension:**
- Python (ms-python.python)

### Why Black Formatting Fails

Black fails when code doesn't meet its strict standards:

❌ **Common Issues:**
```python
# Too long lines (>88 chars default, >100 in our config)
def very_long_function_name_with_many_parameters(param1, param2, param3, param4, param5, param6):
    pass

# Missing spaces
x=1+2

# Inconsistent quotes
message = "Hello" + 'World'

# Wrong trailing commas
data = [
    1,
    2,
    3  # Missing comma
]
```

✅ **After Black:**
```python
# Properly wrapped
def very_long_function_name_with_many_parameters(
    param1, param2, param3, param4, param5, param6
):
    pass

# Proper spacing
x = 1 + 2

# Consistent quotes
message = "Hello" + "World"

# Trailing commas
data = [
    1,
    2,
    3,
]
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=instantgrade tests/

# Run specific test file
pytest tests/test_evaluator.py

# Or use Makefile
make test
```

## Before Committing

Always run these commands before committing:

```bash
# Format code
make format

# Run all checks (formatting + linting)
make check

# Or use the combined command
make pre-commit
```

If you have pre-commit hooks installed, this happens automatically!

## CI/CD Pipeline

Our GitHub Actions workflows check:
1. **Code Formatting** - Black must pass
2. **Linting** - Flake8 must pass
3. **Tests** - All tests must pass
4. **Multi-Platform** - Tests on Ubuntu, Windows, macOS
5. **Multi-Python** - Tests on Python 3.10, 3.11, 3.12

To simulate CI locally:
```bash
make ci-check
```

## Common Issues and Solutions

### Issue 1: Black Formatting Fails in CI

**Problem:** You committed code, but CI fails with black formatting errors.

**Solution:**
```bash
# Format the code
python3 -m black src/

# Commit the formatted code
git add src/
git commit -m "Format code with black"
git push
```

**Prevention:** Install pre-commit hooks (see above).

### Issue 2: Import Errors

**Problem:** Can't import instantgrade module.

**Solution:**
```bash
# Reinstall in development mode
pip install -e .
```

### Issue 3: Tests Fail Locally

**Problem:** Tests pass in CI but fail locally.

**Solution:**
```bash
# Make sure you have test dependencies
pip install -e ".[test]"

# Clean and reinstall
make clean
pip install -e ".[dev]"
```

### Issue 4: Documentation Build Fails

**Problem:** `make docs` fails.

**Solution:**
```bash
# Install documentation dependencies
pip install -e ".[docs]"

# Clean and rebuild
cd docs
make clean
make html
```

## Code Style Guidelines

### 1. Use Black for Formatting
- Never manually adjust formatting
- Let Black handle it

### 2. Write NumPy-Style Docstrings
```python
def my_function(param1, param2):
    """Short description.
    
    Longer description explaining what the function does.
    
    Parameters
    ----------
    param1 : str
        Description of param1.
    param2 : int
        Description of param2.
    
    Returns
    -------
    bool
        Description of return value.
    
    Examples
    --------
    >>> my_function("test", 42)
    True
    """
    pass
```

### 3. Type Hints
Always include type hints for function parameters and return values:

```python
from pathlib import Path
from typing import List, Optional

def load_files(directory: Path, pattern: str = "*.ipynb") -> List[Path]:
    """Load files from directory."""
    pass
```

### 4. Imports Organization
```python
# Standard library
import json
from pathlib import Path

# Third-party
import pandas as pd
import nbformat

# Local imports
from instantgrade.utils import load_notebook
```

## Git Workflow

```bash
# Create a feature branch
git checkout -b feature/my-feature

# Make changes and format
make format

# Check everything
make check

# Commit (pre-commit hooks run automatically)
git add .
git commit -m "Add my feature"

# Push
git push origin feature/my-feature

# Create pull request on GitHub
```

## Useful Commands

```bash
# Format all code
make format

# Check formatting and linting
make check

# Run tests
make test

# Build docs
make docs

# Clean build artifacts
make clean

# Install package
make install

# Run pre-commit checks
make pre-commit

# Simulate CI checks
make ci-check
```

## Getting Help

- **Documentation:** https://chandraveshchaudhari.github.io/instantgrade/
- **Issues:** https://github.com/chandraveshchaudhari/instantgrade/issues
- **Discussions:** https://github.com/chandraveshchaudhari/instantgrade/discussions

## Summary

To avoid formatting errors in the future:

1. ✅ Install pre-commit hooks: `pre-commit install`
2. ✅ Use VS Code with auto-format on save
3. ✅ Run `make format` before committing
4. ✅ Run `make check` to verify formatting
5. ✅ Let the tools handle formatting - don't fight them!

The key is to **let Black format your code automatically** rather than manually formatting. This ensures consistency and prevents CI failures.

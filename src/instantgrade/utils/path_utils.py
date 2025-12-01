"""Path utilities for file and folder operations.

This module provides utility functions for working with file paths,
detecting file types, and handling filesystem operations.
"""

from pathlib import Path
from typing import List


def list_files_paths(path: Path) -> List[Path]:
    """List all files in the given directory.
    
    Parameters
    ----------
    path : Path
        Directory path to list files from.
    
    Returns
    -------
    list of Path
        List of Path objects for all files in the directory.
        Returns empty list if path doesn't exist or isn't a directory.
    
    Examples
    --------
    >>> from pathlib import Path
    >>> files = list_files_paths(Path("submissions/"))
    >>> print(f"Found {len(files)} files")
    """
    if path.exists() and path.is_dir():
        return [item for item in path.iterdir() if item.is_file()]
    return []


def is_notebook(path: Path) -> bool:
    """Check if a file is a Jupyter notebook.
    
    Parameters
    ----------
    path : Path
        File path to check.
    
    Returns
    -------
    bool
        True if the file has a .ipynb extension, False otherwise.
    
    Examples
    --------
    >>> from pathlib import Path
    >>> is_notebook(Path("notebook.ipynb"))
    True
    >>> is_notebook(Path("script.py"))
    False
    """
    return get_file_extension(path) == ".ipynb"


def is_excel(path: Path) -> bool:
    """Check if a file is an Excel workbook.
    
    Parameters
    ----------
    path : Path
        File path to check.
    
    Returns
    -------
    bool
        True if the file has a .xlsx or .xlsm extension, False otherwise.
    
    Examples
    --------
    >>> from pathlib import Path
    >>> is_excel(Path("data.xlsx"))
    True
    >>> is_excel(Path("data.csv"))
    False
    """
    return get_file_extension(path) in [".xlsx", ".xlsm"]


def get_file_extension(path: Path) -> str:
    """Get the lowercase file extension of a path.
    
    Parameters
    ----------
    path : Path
        File path to extract extension from.
    
    Returns
    -------
    str
        Lowercase file extension including the dot (e.g., '.ipynb'),
        or empty string if no extension or path has no suffix attribute.
    
    Examples
    --------
    >>> from pathlib import Path
    >>> get_file_extension(Path("notebook.ipynb"))
    '.ipynb'
    >>> get_file_extension(Path("README"))
    ''
    """
    return path.suffix.lower() if hasattr(path, "suffix") else ""


def filename_safe_timestamp_format() -> str:
    """Generate a filename-safe timestamp string.
    
    Creates a timestamp string suitable for use in filenames, formatted
    as YYYYMMDD_HHMMSS.
    
    Returns
    -------
    str
        Timestamp string in the format 'YYYYMMDD_HHMMSS'.
    
    Examples
    --------
    >>> timestamp = filename_safe_timestamp_format()
    >>> print(f"report_{timestamp}.html")
    report_20251201_143022.html
    """
    from datetime import datetime

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return timestamp

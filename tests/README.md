This repository already contains a small set of tests that demonstrate the
expected behaviors and serve as runnable examples. The core tests to inspect
are:

- `tests/test_python_flow.py` — local (no-Docker) evaluator example that runs
	an `InstantGrader` and writes an HTML report (with CSV fallback).
- `tests/test_python_flow_docker.py` — Docker-backed integration test (this
	test is skipped automatically if Docker isn't available on the host).
- `tests/test_excel_flow.py` — Excel evaluator example with HTML/CSV fallback.

Run tests locally after installing dev dependencies with:

```
pip install -e '.[dev]'
pytest tests/ -v
```

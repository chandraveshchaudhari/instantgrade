<!-- .github/copilot-instructions.md -->
# InstantGrade — quick onboarding for code assistants

Purpose: give an AI coding agent the minimal, actionable knowledge to be productive in this repository.

1) Big picture
- InstantGrade automates grading for Python Jupyter notebooks and Excel files. The router is `InstantGrader` (see `src/instantgrade/core/orchestrator.py`) which delegates to evaluator implementations:
  - Python notebooks: `src/instantgrade/evaluators/python/evaluator.py` (main pipeline)
  - Excel: `src/instantgrade/evaluators/excel/` (newer, similar pattern)
- Python grading workflow:
  1. `SolutionIngestion` parses instructor `.ipynb` into a question spec (`questions`, `metadata`, `summary`) — see `src/instantgrade/evaluators/python/ingestion/solution_ingestion.py`.
  2. Each student notebook is executed (Docker sandbox via `ExecutionServiceDocker` or locally via `NotebookExecutor`). See `src/instantgrade/evaluators/python/execution_service_docker.py` and `src/instantgrade/evaluators/python/notebook_executor.py`.
  3. `grader.py` (container entrypoint at `src/instantgrade/evaluators/python/execution/resources/grader.py`) runs assertions using `ComparisonService` and writes `/workspace/results.json`.

2) Important file / data-format conventions
- Solution notebook format (detected by `SolutionIngestion`):
  - Markdown heading starting with "##" (two hashes) → treated as question description
  - Next code cell should contain the function definition
  - Following code cell contains tests: lines starting with `assert ` are test assertions; non-assert lines are recorded as `context_code` (setup code)
- Assertions are plain `assert` statements. `ComparisonService` (`src/instantgrade/evaluators/python/comparison/comparison_service.py`) understands `assert <expr> == <expr>` and will extract Expected vs Actual to produce helpful diffs.
- Instructor metadata: define `name` and `roll_number` in a code cell to provide defaults. If student notebook does not set personalized values (or leaves instructor defaults), grading will emit a fatal identity failure and skip assertions.
- Docker grading writes `results.json` with shape: `{"student": {..}, "results": [ {question, assertion, status, error, score, description}, ... ], "execution_errors": [...] }`.

3) Developer workflows & quick commands
- Run tests: `make test` (or `pytest tests/ -v`). See `Makefile` and `setup.py` extras for `dev`/`test` dependencies.
- Run a single local notebook evaluation (no Docker): instantiate `InstantGrader(..., use_docker=False)` in python (see `tests/test_python_flow.py` for an example).
- Build Docker image used for sandboxed grading: `python tools/docker_build_image.py` (tags with current git SHA). The Docker build is also triggered automatically by the runtime when missing.
- Force container rebuild at runtime: set `instantgrade_FORCE_REBUILD=1` or pass debug/force flags in code paths that call the builder.
- For fast iteration during development, bind-mount the repo `src` into the container instead of rebuilding the image.

4) Timeouts & sandboxing
- Per-question timeout: env `QUESTION_TIMEOUT` inside the grader (default 20s). ExecutionServiceDocker and NotebookExecutor provide per-student and per-cell timeouts (configurable in code).
- Inputs and dangerous calls are patched inside containers: `input()` is replaced, `os.kill` is disabled (see `grader.py`). If a student's notebook blocks or crashes, grader collects errors and continues where possible.

5) Testing & common failure modes
- `results.json` not created: usually a hard timeout or runtime crash in the container — check container stdout (host logs contain captured lines) and `ExecutionServiceDocker` timeouts.
- Missing student identity (name/roll_number) produces a single failing `_identity_check_` assertion — tests rely on this behavior (`tests/test_python_flow.py`).
- `ComparisonService` produces rich diffs for lists, dicts, tuples and strings; prefer writing assertions in the `assert <actual> == <expected>` form to get better diagnostics.

6) Project-specific patterns to follow
- Lazy package-level imports: `src/instantgrade/__init__.py` exposes heavy classes lazily (use `from instantgrade import InstantGrader` or `from instantgrade import Evaluator` to avoid import-time side effects).
- Solution tests are authoritative: add instructor hints and `assert`-based tests in solution notebooks to teach the grader how to evaluate student submissions.
- When adding new evaluator features, keep the `grader.py` contract in mind: it must still output `results.json` as above so `ExecutionServiceDocker` can parse results.

7) Useful files to inspect when making changes
- Router / entry: `src/instantgrade/core/orchestrator.py`
- Python evaluator: `src/instantgrade/evaluators/python/evaluator.py`
- Ingestion: `src/instantgrade/evaluators/python/ingestion/solution_ingestion.py`
- Comparison logic: `src/instantgrade/evaluators/python/comparison/comparison_service.py`
- Docker builder & runner: `tools/docker_build_image.py`, `src/instantgrade/evaluators/python/execution_service_docker.py`, `src/instantgrade/evaluators/python/execution/resources/grader.py`
- Notebook execution helpers: `src/instantgrade/evaluators/python/notebook_executor.py`
- Tests: `tests/` (example usage and expected behaviors)
  - See `tests/test_python_flow.py` for a local (no-Docker) evaluator example that runs an `InstantGrader` and writes an HTML report (with CSV fallback).
  - See `tests/test_python_flow_docker.py` for a Docker-backed integration test (skips when Docker is not available).
  - See `tests/test_excel_flow.py` for an Excel evaluator example and HTML/CSV fallback behavior.

If any section is unclear or you'd like more examples (e.g., a sample solution notebook annotated with the expected pattern), tell me which part to expand.

# Installation

This page explains how to install InstantGrade, when Docker is required, and how to choose between local and Docker-backed notebook grading.

## Install from PyPI

The simplest installation is from PyPI:

```bash
python3 -m pip install instantgrade
```

After installation, launch the UI with:

```bash
instantgrade launch
```

If port `8501` is already in use, InstantGrade automatically falls back to the next free port and prints the final URL.

## Choose an execution mode

### Local mode

Use local mode when:

- Docker is not installed
- Docker is installed but the daemon is not running
- You want notebook execution to use the current Python environment directly

Local mode does not require Docker.

### Docker mode

Use Docker mode when:

- You want isolated notebook execution
- You want more reproducible grading across machines
- Student notebooks depend on an execution sandbox separate from the host

Docker mode requires Docker to be installed and available.

## Install Docker for Docker mode

- macOS and Windows: install Docker Desktop from https://www.docker.com/products/docker-desktop
- Linux: install Docker Engine from https://docs.docker.com/engine/install/

Verify that Docker is installed and running:

```bash
docker --version
docker info
```

If these commands fail, use local execution instead of Docker execution.

## Development installation

To work on the code locally in editable mode:

```bash
git clone https://github.com/chandraveshchaudhari/instantgrade.git
cd instantgrade
python3 -m pip install -e .
```

This reflects changes in `src/` immediately without reinstalling the package.

## Optional extras

Install Excel extras:

```bash
python3 -m pip install xlwings
```

Install development dependencies:

```bash
python3 -m pip install -e .[dev]
```

## Docker image refresh after upgrades

When you upgrade InstantGrade, older local Docker images can become stale. If Docker mode behaves as if it is still running older code, rebuild the image.

### Repository workflow

From a cloned repository:

```bash
python tools/docker_build_image.py
python tools/docker_build_image.py --force
```

### Runtime rebuild workflow

For a one-off rebuild during execution:

```bash
instantgrade_FORCE_REBUILD=1 instantgrade launch
```

## What gets installed

After installation you can:

- Run `instantgrade launch` to open the UI
- Import `InstantGrader` or evaluator classes from Python
- Grade notebooks locally or in Docker
- Grade Excel submissions with the Excel evaluator

## Next steps

- Continue with the Quick Start for the first end-to-end grading flow
- Read the Usage Guide for UI features, uploads, and grading workflows

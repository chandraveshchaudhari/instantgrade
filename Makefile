.PHONY: format check test clean install docs

# Format code with black
format:
	@echo "Formatting code with black..."
	python3 -m black src/

# Check code formatting without changing files
check:
	@echo "Checking code formatting..."
	python3 -m black --check src/
	@echo "Linting with flake8..."
	python3 -m flake8 src/ --max-line-length=100 --extend-ignore=E203,W503

# Run tests
test:
	@echo "Running tests..."
	pytest tests/ -v

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Install package in development mode
install:
	@echo "Installing package in development mode..."
	pip install -e ".[dev]"

# Build documentation
docs:
	@echo "Building documentation..."
	cd docs && make html

# Format and check before commit
pre-commit: format check
	@echo "✅ Code is formatted and checked!"

# Run all checks like CI does
ci-check: check test
	@echo "✅ All CI checks passed!"

# Quick Reference: Preventing Black Formatting Errors

## 🚨 Why Black Errors Happen

Black formatting errors occur when your code doesn't follow Black's strict formatting rules. The CI pipeline runs `black --check` which fails if code isn't properly formatted.

## ✅ Quick Fix (When CI Fails)

```bash
# Format all code with black
python3 -m black src/

# Commit and push
git add src/
git commit -m "Format code with black"
git push
```

## 🛠️ Setup Once, Never Worry Again

### Method 1: Pre-Commit Hooks (Recommended)

Install pre-commit hooks that **automatically** format code before each commit:

```bash
# Install pre-commit
pip install pre-commit

# Activate the hooks
pre-commit install

# Test it
pre-commit run --all-files
```

**Now every `git commit` will auto-format your code!**

### Method 2: Use the Makefile

```bash
# Format code before committing
make format

# Check if formatting is correct
make check

# Do both
make pre-commit
```

### Method 3: VS Code Auto-Format

The `.vscode/settings.json` file (already created) configures VS Code to:
- Auto-format on save
- Use Black as formatter

Just save your files and they'll be formatted automatically!

## 📝 Common Workflow

### Before Every Commit:

**Option A - If you have pre-commit hooks:**
```bash
git add .
git commit -m "Your message"  # Formatting happens automatically!
```

**Option B - If you don't have pre-commit hooks:**
```bash
make format  # Format the code
git add .
git commit -m "Your message"
git push
```

## 🔍 Check Before Pushing

```bash
# Run the same checks as CI
make ci-check
```

This runs:
- Black formatting check
- Flake8 linting
- All tests

If this passes locally, CI will pass on GitHub!

## 📚 More Information

See [DEVELOPMENT.md](DEVELOPMENT.md) for complete development guide.

## Summary

**The Problem:** Black enforces strict formatting rules. Manual coding often violates these rules.

**The Solution:** Let Black auto-format your code before committing.

**Best Practice:** Install pre-commit hooks once, never think about formatting again!

```bash
pip install pre-commit && pre-commit install
```

Done! ✨

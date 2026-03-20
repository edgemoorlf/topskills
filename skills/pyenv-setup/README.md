# Python Virtual Environment Setup Skill

Quick reference for setting up Python virtual environments using `uv`.

## Quick Start

```bash
# Create a new virtual environment
uv venv

# Create with specific Python version
uv venv --python 3.11

# Activate (Unix/Mac)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate

# Install packages
uv pip install <package>

# Install from requirements.txt
uv pip install -r requirements.txt
```

## Common Workflows

### New Project Setup
```bash
cd my-project
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### Existing Project
```bash
cd existing-project
# If .venv exists:
source .venv/bin/activate

# If .venv missing:
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### Install Single Package
```bash
source .venv/bin/activate
uv pip install requests
```

### Install Without Activating
```bash
# Use the venv Python directly
.venv/bin/python -m pip install <package>

# Or with uv
uv pip install --python .venv/bin/python <package>
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `uv: command not found` | Install uv: `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| `No virtual environment found` | Run `uv venv` first |
| `Permission denied` | Use `source .venv/bin/activate` not `.venv/bin/activate` |
| Package not found after install | Make sure venv is activated |

## Why uv?

- **Fast**: 10-100x faster than pip
- **Reliable**: Better dependency resolution
- **Universal**: Works on all platforms
- **Compatible**: Drop-in replacement for pip

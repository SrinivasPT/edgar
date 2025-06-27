# Scripts Consolidation - Why Only pyproject.toml?

## The Problem with Two Configuration Files

Having both `scripts.toml` and `pyproject.toml` was redundant and went against Python best practices:

### Issues:
1. **Duplication**: Same information in multiple places
2. **Maintenance**: Need to update both files when adding scripts  
3. **Confusion**: Developers don't know which file to check
4. **Non-standard**: `scripts.toml` is not a Python standard

## The Solution: Single Source of Truth

### ✅ **New Approach**: `pyproject.toml` + `dev.py`

1. **`pyproject.toml`** - Contains all standard Python project configuration:
   - Package metadata
   - Dependencies  
   - Console scripts (`edgar`, `edgar-api`, `edgar-web`)
   - Tool configuration (ruff, mypy, pytest)

2. **`dev.py`** - Simple task runner for development workflows:
   - Cross-platform Python script
   - No external dependencies
   - Self-documenting with `--help`

## Benefits

### 🎯 **Standard Python Practices**
- Single `pyproject.toml` follows PEP 518/621 standards
- No custom configuration files
- Better IDE and tool support

### 🚀 **Better Developer Experience**
```bash
# Old way (confusing)
uv run --script test        # From scripts.toml
edgar-api                   # From pyproject.toml

# New way (consistent)  
python dev.py test         # Development tasks
edgar-api                  # Production commands
```

### 🧹 **Cleaner Project Structure**
```
pyproject.toml    # ✅ Single source of configuration
dev.py           # ✅ Simple development task runner
# scripts.toml    # ❌ Removed (redundant)
```

### 📖 **Self-Documenting**
```bash
python dev.py             # Shows all available tasks
python dev.py qa          # Runs complete quality checks
```

## Usage Examples

### Development Tasks
```bash
python dev.py test        # Run tests
python dev.py lint-fix    # Fix code issues
python dev.py qa          # Full quality check
python dev.py setup-data  # Create directories
```

### Production Commands (from pyproject.toml)
```bash
edgar                     # CLI tool
edgar-api                 # API server
edgar-web                 # Web server
```

## Migration Complete

✅ Removed redundant `scripts.toml`
✅ Consolidated all configuration into `pyproject.toml`  
✅ Created `dev.py` for development workflows
✅ Updated documentation

**Result**: Clean, standard Python project configuration! 🎉

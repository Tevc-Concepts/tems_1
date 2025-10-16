# TEMS AI Module - Dependencies Management

## Overview

The `tems_ai` module's dependencies are **bundled with the TEMS app** via `pyproject.toml`. This ensures that when TEMS is installed on any Frappe/ERPNext platform, all required packages are automatically installed.

## Bundled Dependencies

These packages are declared in `/apps/tems/pyproject.toml` and are **automatically installed** with TEMS:

### Core Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| **numpy** | >=1.24.0 | Numerical computations, array operations, metrics calculations |
| **scikit-learn** | >=1.3.0 | ML preprocessing, model evaluation, data transformations |
| **requests** | (via Frappe) | HTTP requests for external API model calls |

### Why These Dependencies?

1. **numpy**: Used extensively in:
   - `tems_ai/utils/metrics.py` - MAE, RMSE, accuracy calculations
   - `tems_ai/utils/preprocessor.py` - Feature normalization and scaling
   - All handler modules for numerical computations

2. **scikit-learn**: Used for:
   - Data preprocessing (StandardScaler, LabelEncoder)
   - Model evaluation metrics
   - Future local ML model implementations
   - Train/test splitting and validation

3. **requests**: Used in:
   - `tems_ai/services/model_manager.py` - External API model predictions
   - OpenAI, Azure ML, Hugging Face integrations

## Optional Dependencies

These are NOT bundled and must be installed manually if needed:

### Deep Learning (Optional)

```bash
./env/bin/pip install tensorflow>=2.13.0
# OR
./env/bin/pip install torch>=2.0.0
```

**Use case**: Advanced predictive models, image processing (for spot check photos), NLP for driver feedback analysis.

### Advanced NLP (Optional)

```bash
./env/bin/pip install transformers>=4.30.0
```

**Use case**: Sentiment analysis on driver feedback, automated report generation.

## Installation Flow

### New TEMS Installation

When installing TEMS on a new site:

```bash
# 1. Get the app (downloads code + declares dependencies)
bench get-app tems

# 2. Install on site (automatically installs numpy, scikit-learn)
bench --site <site-name> install-app tems
```

During step 2, bench automatically:
1. Reads `tems/pyproject.toml`
2. Installs all dependencies listed
3. Makes them available to the app

### Updating Existing TEMS Installation

```bash
# Update app code
bench update --app tems

# If dependencies were added/updated, reinstall them
./env/bin/pip install -e apps/tems
```

### Manual Dependency Verification

Check installed packages:

```bash
./env/bin/pip list | grep -E "numpy|scikit-learn"
```

Expected output:
```
numpy                    1.24.3
scikit-learn             1.3.2
```

## Platform Portability

### Why Bundling Matters

By declaring dependencies in `pyproject.toml`:

1. **Consistency**: Every installation gets the same versions
2. **Portability**: No manual setup required on new servers
3. **Version Control**: Dependency versions are tracked in git
4. **Bench Compatibility**: Works with standard Frappe bench commands

### Cross-Platform Installation

The same installation commands work on:
- Local development (Docker, native)
- Staging servers
- Production servers
- Cloud deployments (AWS, Azure, GCP)
- Frappe Cloud

```bash
# Same command everywhere:
bench --site <site> install-app tems
```

## Dependency Constraints

### Version Ranges

We use minimum versions (`>=`) to allow flexibility:

```toml
"numpy>=1.24.0"  # Allows 1.24.0, 1.24.1, 1.25.0, etc.
```

**Rationale**:
- Ensures minimum features available
- Allows users to update for security patches
- Prevents breaking older systems

### Python Version

Required: **Python 3.10+**

Declared in `pyproject.toml`:
```toml
requires-python = ">=3.10"
```

This ensures compatibility with:
- Modern type hints (used throughout tems_ai)
- Latest numpy/scikit-learn features
- Frappe v15+ requirements

## Troubleshooting

### Dependencies Not Installing

**Issue**: After `bench install-app tems`, numpy/scikit-learn not found.

**Solution 1**: Manually install dependencies:
```bash
cd /workspace/development/frappe-bench
./env/bin/pip install -e apps/tems
```

**Solution 2**: Check pyproject.toml is intact:
```bash
cat apps/tems/pyproject.toml | grep dependencies
```

### Version Conflicts

**Issue**: Existing app requires different numpy/scikit-learn version.

**Solution**: Check compatibility:
```bash
./env/bin/pip list | grep -E "numpy|scikit"
```

If conflict exists, upgrade to compatible versions:
```bash
./env/bin/pip install --upgrade numpy scikit-learn
```

### Import Errors

**Issue**: `ModuleNotFoundError: No module named 'numpy'`

**Check 1**: Verify environment:
```bash
which python3  # Should be bench/env/bin/python3
```

**Check 2**: Verify installation:
```bash
./env/bin/python3 -c "import numpy; print(numpy.__version__)"
```

**Fix**: Reinstall:
```bash
./env/bin/pip install numpy scikit-learn
```

## Development vs Production

### Development

During development, you may want bleeding-edge versions:

```bash
./env/bin/pip install --upgrade numpy scikit-learn
```

### Production

In production, pin exact versions for stability:

Edit `pyproject.toml`:
```toml
dependencies = [
    "numpy==1.24.3",  # Pin exact version
    "scikit-learn==1.3.2",
]
```

Then lock dependencies:
```bash
./env/bin/pip freeze > apps/tems/requirements-lock.txt
```

## Future Dependencies

As `tems_ai` evolves, additional dependencies may be added:

### Planned (Not Yet Included)

| Package | Purpose | Status |
|---------|---------|--------|
| pandas | Advanced data manipulation | Under consideration |
| opencv-python | Image processing for spot checks | Optional |
| xgboost | Advanced ML models | Optional |
| prophet | Time series forecasting | Under consideration |

### Adding New Dependencies

To add a new required dependency:

1. Edit `pyproject.toml`:
```toml
dependencies = [
    "numpy>=1.24.0",
    "scikit-learn>=1.3.0",
    "pandas>=2.0.0",  # NEW
]
```

2. Test installation:
```bash
./env/bin/pip install -e apps/tems
```

3. Update this document
4. Update INSTALLATION.md
5. Commit changes

## Summary

✅ **Bundled with TEMS**: numpy, scikit-learn  
✅ **Auto-installed**: Yes, via `bench install-app tems`  
✅ **Cross-platform**: Works on all Frappe deployments  
✅ **Version-controlled**: Declared in `pyproject.toml`  
✅ **Portable**: No manual setup needed  

❌ **NOT bundled**: TensorFlow, PyTorch (too large, optional)  
❌ **Manual install required**: Deep learning packages  

## Support

For dependency issues:
- Check bench logs: `bench --site <site> console`
- Verify environment: `./env/bin/pip list`
- Contact: code@tevcng.com

#!/bin/bash
# TEMS AI Module - Dependency Verification Script
# This script verifies that tems_ai dependencies are correctly bundled and installed

set -e  # Exit on error

BENCH_DIR="/workspace/development/frappe-bench"
cd "$BENCH_DIR"

echo "=========================================="
echo "TEMS AI Dependency Verification"
echo "=========================================="
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check 1: Verify pyproject.toml declares dependencies
echo "✓ Check 1: Verifying pyproject.toml..."
if grep -q "numpy>=1.24.0" apps/tems/pyproject.toml && grep -q "scikit-learn>=1.3.0" apps/tems/pyproject.toml; then
    echo -e "${GREEN}✓ Dependencies declared in pyproject.toml${NC}"
    grep -A 3 'dependencies = \[' apps/tems/pyproject.toml
else
    echo -e "${RED}✗ Dependencies NOT found in pyproject.toml${NC}"
    exit 1
fi
echo ""

# Check 2: Verify dependencies are installed
echo "✓ Check 2: Verifying installed packages..."
if ./env/bin/pip list | grep -q "numpy"; then
    NUMPY_VERSION=$(./env/bin/pip show numpy | grep Version | awk '{print $2}')
    echo -e "${GREEN}✓ numpy installed: $NUMPY_VERSION${NC}"
else
    echo -e "${YELLOW}⚠ numpy NOT installed (will be installed on next app install)${NC}"
fi

if ./env/bin/pip list | grep -q "scikit-learn"; then
    SKLEARN_VERSION=$(./env/bin/pip show scikit-learn | grep Version | awk '{print $2}')
    echo -e "${GREEN}✓ scikit-learn installed: $SKLEARN_VERSION${NC}"
else
    echo -e "${YELLOW}⚠ scikit-learn NOT installed (will be installed on next app install)${NC}"
fi
echo ""

# Check 3: Test imports
echo "✓ Check 3: Testing imports..."
if ./env/bin/python3 -c "import numpy; print(f'numpy {numpy.__version__} imports successfully')" 2>/dev/null; then
    echo -e "${GREEN}✓ numpy imports successfully${NC}"
else
    echo -e "${YELLOW}⚠ numpy import failed (install with: ./env/bin/pip install -e apps/tems)${NC}"
fi

if ./env/bin/python3 -c "import sklearn; print(f'scikit-learn {sklearn.__version__} imports successfully')" 2>/dev/null; then
    echo -e "${GREEN}✓ scikit-learn imports successfully${NC}"
else
    echo -e "${YELLOW}⚠ scikit-learn import failed (install with: ./env/bin/pip install -e apps/tems)${NC}"
fi
echo ""

# Check 4: Verify tems_ai module can import dependencies
echo "✓ Check 4: Testing tems_ai module imports..."
IMPORT_TEST=$(./env/bin/python3 << 'EOF'
import sys
sys.path.insert(0, 'apps')

try:
    # Test core imports
    import numpy as np
    from sklearn.preprocessing import StandardScaler
    
    # Test tems_ai imports
    from tems.tems_ai.utils.metrics import calculate_accuracy
    from tems.tems_ai.utils.preprocessor import normalize_numeric_features
    
    print("✓ All tems_ai imports successful")
    print(f"  - numpy: {np.__version__}")
    import sklearn
    print(f"  - scikit-learn: {sklearn.__version__}")
    exit(0)
except ImportError as e:
    print(f"✗ Import error: {e}")
    exit(1)
EOF
)

if [ $? -eq 0 ]; then
    echo -e "${GREEN}$IMPORT_TEST${NC}"
else
    echo -e "${RED}$IMPORT_TEST${NC}"
    echo -e "${YELLOW}To fix: ./env/bin/pip install -e apps/tems${NC}"
fi
echo ""

# Check 5: Verify documentation exists
echo "✓ Check 5: Verifying documentation..."
DOCS=(
    "apps/tems/tems/tems_ai/README.md"
    "apps/tems/tems/tems_ai/INSTALLATION.md"
    "apps/tems/tems/tems_ai/DEPENDENCIES.md"
    "apps/tems/tems/tems_ai/API_REFERENCE.md"
    "apps/tems/tems/tems_ai/EXAMPLES.md"
)

for doc in "${DOCS[@]}"; do
    if [ -f "$doc" ]; then
        echo -e "${GREEN}✓ ${doc}${NC}"
    else
        echo -e "${RED}✗ ${doc} NOT FOUND${NC}"
    fi
done
echo ""

# Summary
echo "=========================================="
echo "Summary"
echo "=========================================="
echo ""
echo "Dependencies Status:"
echo "  - Declared in pyproject.toml: ✓"
echo "  - Installation method: Auto (via bench install-app tems)"
echo "  - Required packages: numpy>=1.24.0, scikit-learn>=1.3.0"
echo ""
echo "Documentation:"
echo "  - See apps/tems/tems/tems_ai/DEPENDENCIES.md for details"
echo "  - See apps/tems/tems/tems_ai/INSTALLATION.md for setup guide"
echo ""
echo "To install/update dependencies:"
echo "  ./env/bin/pip install -e apps/tems"
echo ""
echo "To verify on a fresh site:"
echo "  bench new-site test.localhost"
echo "  bench --site test.localhost install-app tems"
echo "  ./env/bin/pip list | grep -E 'numpy|scikit-learn'"
echo ""

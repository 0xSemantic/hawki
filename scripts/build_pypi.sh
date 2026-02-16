#!/bin/bash
# --------------------
# File: scripts/build_pypi.sh
# --------------------
set -e

# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build wheel and source distribution
python -m build

# Upload to PyPI (requires twine)
twine upload dist/*
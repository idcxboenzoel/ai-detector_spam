#!/bin/bash

# Stop if any command fails
set -e

# 🟢 Step 1: Bersihkan build sebelumnya
echo "🧹 Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info

# 🟢 Step 2: Build package
echo "📦 Building the package..."
python -m build

# 🟢 Step 3: Upload ke PyPI (ganti dengan test.pypi.org jika perlu)
echo "🚀 Uploading to PyPI..."
twine upload dist/*

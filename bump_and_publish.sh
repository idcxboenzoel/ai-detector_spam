#!/bin/bash

set -e

# === CONFIG ===
REPO="pypi"  # Ubah ke "testpypi" kalau mau default-nya ke TestPyPI
COMMIT_MSG="release: version bump"
GIT_TAG_PREFIX="v"

# === Fungsi bump versi ===
bump_version() {
    old_version=$(sed -nE 's/^version = "([0-9]+\.[0-9]+\.[0-9]+)"/\1/p' pyproject.toml)
    IFS='.' read -r major minor patch <<< "$old_version"

    case "$1" in
        --major)
            new_version="$((major + 1)).0.0"
            ;;
        --minor)
            new_version="$major.$((minor + 1)).0"
            ;;
        --patch|*)
            new_version="$major.$minor.$((patch + 1))"
            ;;
    esac

    echo "🔄 Bumping version: $old_version → $new_version"
    sed -i '' "s/version = \"$old_version\"/version = \"$new_version\"/" pyproject.toml
}

# === Parse argumen ===
version_type="--patch"
upload_repo=$REPO

for arg in "$@"; do
    case "$arg" in
        --major|--minor|--patch)
            version_type="$arg"
            ;;
        --test)
            upload_repo="testpypi"
            ;;
    esac
done

# === Jalankan semua proses ===
echo "🧹 Cleaning build artifacts..."
rm -rf dist/ build/ *.egg-info

echo "🔄 Updating version..."
bump_version "$version_type"

new_version=$(sed -nE 's/^version = "([0-9]+\.[0-9]+\.[0-9]+)"/\1/p' pyproject.toml)

echo "📦 Building package..."
python -m build

echo "🚀 Uploading to $upload_repo..."
if [ "$upload_repo" = "testpypi" ]; then
    twine upload --repository testpypi dist/*
else
    twine upload dist/*
fi

echo "📌 Committing & tagging..."
git add pyproject.toml
git commit -m "$COMMIT_MSG $new_version"
git tag "${GIT_TAG_PREFIX}${new_version}"
git push
git push --tags

echo "✅ Done. Version: $new_version"

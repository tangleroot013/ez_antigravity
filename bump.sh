#!/bin/bash
# Usage: ./bump.sh patch | minor | major
TYPE=$1

if [[ "$TYPE" != "patch" && "$TYPE" != "minor" && "$TYPE" != "major" ]]; then
    echo "Usage: ./bump.sh [patch|minor|major]"
    exit 1
fi

# Extract version from pyproject.toml (Assuming version = "0.1.0")
VERSION=$(grep "version =" pyproject.toml | cut -d '"' -f 2)
IFS='.' read -r major minor patch <<< "$VERSION"

case $TYPE in
    patch) patch=$((patch + 1)) ;;
    minor) minor=$((minor + 1)); patch=0 ;;
    major) major=$((major + 1)); minor=0; patch=0 ;;
esac

NEW_VERSION="$major.$minor.$patch"
sed -i "s/version = \"$VERSION\"/version = \"$NEW_VERSION\"/" pyproject.toml

echo "🚀 Bumping version $VERSION -> $NEW_VERSION"
git add pyproject.toml
git commit -m "CHORE: Bump version to $NEW_VERSION"
git tag -a "v$NEW_VERSION" -m "Release v$NEW_VERSION"
git push origin main --tags

echo "✅ Version $NEW_VERSION deployed. Quack!"

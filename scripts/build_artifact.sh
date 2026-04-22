#!/usr/bin/env bash
set -euo pipefail

APP_NAME="${APP_NAME:-recipe-recommender}"
VERSION="${VERSION:-$(git rev-parse --short HEAD 2>/dev/null || echo local)}"
DIST_DIR="${DIST_DIR:-dist}"
BUILD_DIR="${BUILD_DIR:-build}"
PACKAGE_DIR="${BUILD_DIR}/${APP_NAME}"
ARTIFACT_PATH="${DIST_DIR}/${APP_NAME}-${VERSION}.tar.gz"

rm -rf "$PACKAGE_DIR"
mkdir -p "$PACKAGE_DIR" "$DIST_DIR"

cp app.py recommender.py recipes.py requirements.txt README.md "$PACKAGE_DIR"/
cp -R static templates tests scripts "$PACKAGE_DIR"/

{
    echo "app_name=${APP_NAME}"
    echo "version=${VERSION}"
    echo "built_at_utc=$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
    echo "artifact=${ARTIFACT_PATH}"
} > "${PACKAGE_DIR}/BUILD_INFO.txt"

tar -czf "$ARTIFACT_PATH" -C "$BUILD_DIR" "$APP_NAME"
tar -tzf "$ARTIFACT_PATH" > /dev/null

echo "$ARTIFACT_PATH" > "${DIST_DIR}/latest-artifact.txt"
echo "Built artifact: ${ARTIFACT_PATH}"

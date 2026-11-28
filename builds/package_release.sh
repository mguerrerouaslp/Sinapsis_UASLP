#!/usr/bin/env bash
# ==============================================================================
# Sinapsis — Production Release Packaging Utility
# Generates sanitized distribution packages (.zip) and release directories
# purged of operating system metadata (.DS_Store, ._*, Thumbs.db, etc.).
# ==============================================================================

set -euo pipefail

# Resolve repository root path (script resides in builds/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

cd "${REPO_ROOT}"

# Disable macOS AppleDouble file creation during copy/compression
export COPYFILE_DISABLE=1

# 1. Determine release version
if [ -n "${1:-}" ]; then
  VERSION="$1"
  if [[ "$VERSION" =~ ^v ]]; then
    VERSION_TAG="$VERSION"
  else
    VERSION_TAG="v${VERSION}"
  fi
else
  RAW_VER=$(grep -E '^## \[[0-9]+\.[0-9]+' CHANGELOG.md 2>/dev/null | head -n 1 | sed -E 's/## \[([0-9]+\.[0-9]+(\.[0-9]+)?)\].*/\1/' || true)
  if [ -n "$RAW_VER" ]; then
    VERSION_TAG="v${RAW_VER}"
  else
    VERSION_TAG="v0.1.0"
  fi
fi

RELEASE_NAME="Sinapsis_${VERSION_TAG}"
RELEASE_DIR="${REPO_ROOT}/builds/release/${RELEASE_NAME}"
RELEASE_ZIP="${REPO_ROOT}/builds/release/${RELEASE_NAME}.zip"

echo "=================================================="
echo " Packaging Release: ${RELEASE_NAME}"
echo "=================================================="

# 2. Clean operating system artifacts in build folders
echo "-> Purging operating system metadata (.DS_Store, ._*, Thumbs.db)..."
find "${REPO_ROOT}/builds" -name ".DS_Store" -type f -delete 2>/dev/null || true
find "${REPO_ROOT}/builds" -name "._*" -type f -delete 2>/dev/null || true
find "${REPO_ROOT}/builds" -name "Thumbs.db" -type f -delete 2>/dev/null || true

# 3. Prepare release destination directories
rm -rf "${RELEASE_DIR}"
rm -f "${RELEASE_ZIP}"
mkdir -p "${RELEASE_DIR}/otf"
mkdir -p "${RELEASE_DIR}/woff"
mkdir -p "${RELEASE_DIR}/woff2"
mkdir -p "${RELEASE_DIR}/ttf"

# 4. Copy compiled font binaries if present
echo "-> Copying compiled font binaries..."
if compgen -G "${REPO_ROOT}/builds/otf/proof/*.otf" > /dev/null; then
  cp "${REPO_ROOT}/builds/otf/proof/"*.otf "${RELEASE_DIR}/otf/"
fi

if compgen -G "${REPO_ROOT}/builds/ttf/*.ttf" > /dev/null; then
  cp "${REPO_ROOT}/builds/ttf/"*.ttf "${RELEASE_DIR}/ttf/"
fi

if compgen -G "${REPO_ROOT}/builds/woff/proof/*.woff" > /dev/null; then
  cp "${REPO_ROOT}/builds/woff/proof/"*.woff "${RELEASE_DIR}/woff/"
fi

if compgen -G "${REPO_ROOT}/builds/woff2/*.woff2" > /dev/null; then
  cp "${REPO_ROOT}/builds/woff2/"*.woff2 "${RELEASE_DIR}/woff2/"
fi

# Remove empty format directories if no binaries are available yet
for fmt in otf ttf woff woff2; do
  if [ -z "$(ls -A "${RELEASE_DIR}/${fmt}" 2>/dev/null)" ]; then
    rm -rf "${RELEASE_DIR}/${fmt}"
  fi
done

# 5. Copy license and distribution documentation
echo "-> Including licensing and release documentation..."
[ -f "${REPO_ROOT}/EULA.txt" ] && cp "${REPO_ROOT}/EULA.txt" "${RELEASE_DIR}/"
[ -f "${REPO_ROOT}/EULA.md" ] && cp "${REPO_ROOT}/EULA.md" "${RELEASE_DIR}/"
[ -f "${REPO_ROOT}/LICENSE.txt" ] && cp "${REPO_ROOT}/LICENSE.txt" "${RELEASE_DIR}/"
[ -f "${REPO_ROOT}/README.md" ] && cp "${REPO_ROOT}/README.md" "${RELEASE_DIR}/"
[ -f "${REPO_ROOT}/CONTRIBUTORS.md" ] && cp "${REPO_ROOT}/CONTRIBUTORS.md" "${RELEASE_DIR}/"
[ -f "${REPO_ROOT}/CHANGELOG.md" ] && cp "${REPO_ROOT}/CHANGELOG.md" "${RELEASE_DIR}/"

if [ -d "${REPO_ROOT}/docs" ]; then
  mkdir -p "${RELEASE_DIR}/docs"
  cp -R "${REPO_ROOT}/docs/"* "${RELEASE_DIR}/docs/"
fi

if [ -d "${REPO_ROOT}/scripts" ]; then
  mkdir -p "${RELEASE_DIR}/scripts"
  cp -R "${REPO_ROOT}/scripts/"* "${RELEASE_DIR}/scripts/"
fi

# Include only top-level specimens from assets/ (exclude archival assets/scans/)
if [ -d "${REPO_ROOT}/assets" ]; then
  mkdir -p "${RELEASE_DIR}/assets"
  find "${REPO_ROOT}/assets" -maxdepth 1 -type f ! -name ".DS_Store" ! -name "._*" -exec cp {} "${RELEASE_DIR}/assets/" \;
  if [ -z "$(ls -A "${RELEASE_DIR}/assets" 2>/dev/null)" ]; then
    rm -rf "${RELEASE_DIR}/assets"
  fi
fi

# 6. Generate sanitized zip archive
echo "-> Compiling sanitized zip archive..."
(
  cd "${REPO_ROOT}/builds/release"
  zip -r -X -q "${RELEASE_NAME}.zip" "${RELEASE_NAME}"
)

echo "=================================================="
echo " Release successfully generated at:"
echo " ${RELEASE_ZIP}"
echo "=================================================="

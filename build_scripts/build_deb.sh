#!/bin/bash
set -e

# 1. Get Version from defaults.py
# It looks like: BROWSER_VERSION = "0.0.1"
VERSION=$(grep -E "^BROWSER_VERSION" src/defaults.py | sed -E 's/.*["'\'']([^"'\'']+)["'\''].*/\1/')

if [ -z "$VERSION" ]; then
    echo "Error: Could not extract version from src/defaults.py"
    exit 1
fi

echo "Building BogasBogasGo v$VERSION"

PACKAGE_NAME="bogasbogasgo"
ARCH="amd64"
PACKAGE_DIR="${PACKAGE_NAME}_${VERSION}_${ARCH}"

# Create directory structure
mkdir -p "$PACKAGE_DIR/DEBIAN"
mkdir -p "$PACKAGE_DIR/usr/bin"
mkdir -p "$PACKAGE_DIR/usr/share/bogasbogasgo/src"
mkdir -p "$PACKAGE_DIR/usr/share/applications"
mkdir -p "$PACKAGE_DIR/usr/share/icons/hicolor/256x256/apps"

# 2. Copy source code (recursively to include services)
# Clean up pycache first
find src -name "__pycache__" -type d -exec rm -rf {} +
cp -r src/* "$PACKAGE_DIR/usr/share/bogasbogasgo/src/"

# 3. Create launcher script
cat <<EOF > "$PACKAGE_DIR/usr/bin/BogasBogasGo"
#!/bin/bash
export PYTHONPATH=\$PYTHONPATH:/usr/share/bogasbogasgo/src
python3 /usr/share/bogasbogasgo/src/main.py "\$@"
EOF
chmod +x "$PACKAGE_DIR/usr/bin/BogasBogasGo"

# 4. Copy assets
if [ -f "assets/bogasbogasgo.desktop" ]; then
    cp assets/bogasbogasgo.desktop "$PACKAGE_DIR/usr/share/applications/"
else
    echo "Warning: assets/bogasbogasgo.desktop not found"
fi

if [ -f "docs/images/bogasbogasgo-logo.png" ]; then
    cp docs/images/bogasbogasgo-logo.png "$PACKAGE_DIR/usr/share/icons/hicolor/256x256/apps/bogasbogasgo.png"
else
    echo "Warning: docs/images/bogasbogasgo-logo.png not found"
fi

# 5. Create control file
cat <<EOF > "$PACKAGE_DIR/DEBIAN/control"
Package: $PACKAGE_NAME
Version: $VERSION
Section: utils
Priority: optional
Architecture: $ARCH
Maintainer: BogasBogasGo Team
Depends: python3, python3-pyqt6, python3-pyqt6.qtwebengine, python3-pil
Description: Navegador para Ancaps
EOF

# 6. Build the package
dpkg-deb --build "$PACKAGE_DIR"

# 7. Cleanup
rm -rf "$PACKAGE_DIR"

echo "Build complete: ${PACKAGE_DIR}.deb"

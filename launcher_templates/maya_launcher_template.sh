#!/usr/bin/env bash
# Template launcher for Maya on Linux - copy this file, then adjust the
# Maya path/version below to match your own installation. Requires bash.
#
#   cp maya_launcher_template.sh maya_launcher.sh
#   chmod +x maya_launcher.sh
#   ./maya_launcher.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/hdmcg.sh"

MAYA="/usr/autodesk/maya<VERSION>/bin/maya"
# macOS default install location - comment out the line above and use this instead:
# MAYA="/Applications/Autodesk/Maya<VERSION>/Maya.app/Contents/MacOS/Maya"

echo
echo "Maya executable used:"
echo "   $MAYA"
echo "   Version is <VERSION>"
"$MAYA"

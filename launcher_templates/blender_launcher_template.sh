#!/usr/bin/env bash
# Template launcher for Blender on Linux/macOS - copy this file, then adjust
# the paths below to match your own installation. Requires bash.
#
#   cp blender_launcher_template.sh blender_launcher.sh
#   chmod +x blender_launcher.sh
#   ./blender_launcher.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/hdmcg.sh"

# export BLENDER_CUSTOM_SPLASH="/path/to/my_splash.png"

# Only needed for the PySide6-based hdmcg tools.
# Point this at the "site-packages" folder INSIDE your venv (see README).
# Note the "pythonX.Y" folder name depends on the Python version the venv
# was created with - check it with: ls <your venv>/lib/
export BLENDER_PYSIDE="/home/<YOUR_USER_NAME>/venvs/hdmcg/lib/python3.11/site-packages"

# Linux default install location:
BLENDER="/usr/bin/blender"
# macOS default install location - comment out the line above and use this instead:
# BLENDER="/Applications/Blender.app/Contents/MacOS/Blender"

echo
echo "Environment variables set by blender_launcher_template.sh:"
echo
if [ -z "$BLENDER_PYSIDE" ]; then
    echo "BLENDER_PYSIDE is NOT set."
elif [ ! -d "$BLENDER_PYSIDE" ]; then
    echo "WARNING: BLENDER_PYSIDE is set, but the path does not exist:"
    echo "   $BLENDER_PYSIDE"
else
    echo "BLENDER_PYSIDE"
    echo "   $BLENDER_PYSIDE"
fi
echo
echo "Blender executable used:"
echo "   $BLENDER"
echo "   Version is 5.2.1 LTS"
"$BLENDER" --python "$SCRIPT_DIR/hdmcg/blender/bootstrap.py"
echo
read -rp "Press Enter to continue..." _

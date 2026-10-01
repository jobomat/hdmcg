#!/usr/bin/env bash
# Shared environment setup for Linux/macOS - the Unix counterpart of hdmcg.bat.
#
# This script must be SOURCED, not executed, so the variables it exports stay
# set in the calling launcher script (which then starts Maya/Blender):
#   source "$SCRIPT_DIR/hdmcg.sh"
# Running it directly (./hdmcg.sh) would only set the variables in a
# subprocess that exits immediately afterwards - Maya/Blender would never see them.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"
export XBMLANGPATH="$SCRIPT_DIR/resources/maya/icons/:$XBMLANGPATH"
export MAYA_SHELF_PATH="$SCRIPT_DIR/resources/maya/shelves/:$MAYA_SHELF_PATH"
export OCIO="$SCRIPT_DIR/resources/cg-config-v1.0.0_aces-v1.3_ocio-v2.1.ocio"

echo
printf '%s\n' '      ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
printf '%s\n' '      "       _         _                           "'
printf '%s\n' '      "      | |       | |                          "'
printf '%s\n' '      "      | |__   __| |_ __ ___   ___ __ _       "'
printf '%s\n' '      "      | '\''_ \ / _` | '\''_ ` _ \ / __/ _` |      "'
printf '%s\n' '      "      | | | | (_| | | | | | | (_| (_| |      "'
printf '%s\n' '      "      |_| |_|\__,_|_| |_| |_|\___\__, |      "'
printf '%s\n' '      "                                  __/ |      "'
printf '%s\n' '      "                                 |___/       "'
printf '%s\n' '      ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
echo
echo "Environment variables set by hdmcg.sh:"
echo
echo "PYTHONPATH:"
echo "    $PYTHONPATH"
echo
echo "XBMLANGPATH:"
echo "    $XBMLANGPATH"
echo
echo "MAYA_SHELF_PATH:"
echo "    $MAYA_SHELF_PATH"
echo
echo "OCIO:"
echo "    $OCIO"
echo

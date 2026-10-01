@echo off
set PYTHONPATH=%~dp0;%PYTHONPATH%
set XBMLANGPATH=%~dp0resources\maya\icons\
set MAYA_SHELF_PATH=%~dp0resources\maya\shelves\;%MAYA_SHELF_PATH%
set OCIO=%~dp0resources\cg-config-v1.0.0_aces-v1.3_ocio-v2.1.ocio
echo.
echo      ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
echo      "       _         _                           "
echo      "      | |       | |                          "
echo      "      | |__   __| |_ __ ___   ___ __ _       "
echo      "      | '_ \ / _` | '_ ` _ \ / __/ _` |      "
echo      "      | | | | (_| | | | | | | (_| (_| |      "
echo      "      |_| |_|\__,_|_| |_| |_|\___\__, |      "
echo      "                                  __/ |      "
echo      "                                 |___/       "
echo      ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
echo.
echo Environment variables set by hdmcg.bat:
echo.
echo PYTHONPATH:
echo     %PYTHONPATH%
echo.
echo XBMLANGPATH:
echo     %XBMLANGPATH%
echo.
echo MAYA_SHELF_PATH:
echo     %MAYA_SHELF_PATH%
echo.
echo OCIO:
echo     %OCIO%
echo.

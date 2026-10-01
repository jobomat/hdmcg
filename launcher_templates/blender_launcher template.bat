@echo off
call hdmcg.bat
REM set BLENDER_CUSTOM_SPLASH=path\to\my_splash.png
set BLENDER_PYSIDE=C:\Users\<YOUR_USER_NAME>\Documents\venvs\hdmcg\Lib\site-packages
set BLENDER="C:\Program Files\Blender Foundation\Blender 5.2\blender-launcher.exe"

echo Environment variables set by blender_launcher.bat:
echo.
if not defined BLENDER_PYSIDE (
    echo BLENDER_PYSIDE ist NICHT gesetzt.
) else if not exist "%BLENDER_PYSIDE%" (
    echo WARNUNG: BLENDER_PYSIDE ist gesetzt, aber der Pfad existiert nicht:
    echo    %BLENDER_PYSIDE%
) else (
    echo BLENDER_PYSIDE
    echo    %BLENDER_PYSIDE%
)
echo.
echo Blender Executable used:
echo    %BLENDER%
echo    Version is 5.2.1 LTS
%BLENDER% --python %~dp0\hdmcg\blender\bootstrap.py
echo.
pause
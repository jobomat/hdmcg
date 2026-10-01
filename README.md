# hdmcg

## What is this?

`hdmcg` is a collection of small tools for 3D-DCCs (at the moment mostly Maya),
written once in Python and partly shared between programs. 

A couple of Tools rely on **PySide6**. In Blender that needs one extra
setup step (explained below).

## What you need to do, in short

- [ ] Get the `hdmcg` folder onto your computer (clone or download and unzip)
- [ ] **All DCCs**: create a launcher
- [ ] **Blender with PySide-Tools** (Optional): Install Python, create a venv, install PySide6 into it, point the Blender launcher at it

Each of these is explained step by step below.

## Installation

Put the whole `hdmcg` folder somewhere on your PC, e.g. directly under `C:\hdmcg`. Avoid folders with spaces, umlauts (ä, ö, ü) or German characters in the path if you can as some tools get confused by that.

Everything below assumes you're inside that folder in a terminal (powershell/bash) when editing the `.bat`/`.sh` files.

## Set up Launchers for all DCCs

Make yourself a DCC launcher based on the templates located in `launcher_templates` (e.g. `maya_launcher_template.bat` for Windows, `maya_launcher_template.sh` for Mac/Linux). Copy the template **out of that folder to the repo root**, next to `hdmcg.bat`/`hdmcg.sh`, then edit it so it matches **your** DCC installation. It should at least contain the calling of `hdmcg.bat` (or hdmcg.sh for Linux and Mac) and the DCC executable. Example for Maya on Windows (for Linux and Mac use the corresponding *.sh files and **read the comments in the sh-files**!):

```bat
@echo off
call hdmcg.bat

"C:\Program Files\Autodesk\Maya2027\bin\maya.exe"
```

Keep your launcher next to `hdmcg.bat`/`hdmcg.sh` (e.g. as `maya_launcher.bat`) and double-click it to start the DCC with hdmcg loaded.

**Linux/macOS only:** `.sh` files need the executable bit set before they can be run. Plain copies (`cp`) or a fresh `git clone` don't always keep it. Set it once per launcher you create to be sure:

```bash
chmod +x maya_launcher.sh
```

Then start it with `./maya_launcher.sh` (or double-click it, if your file manager is set up to run `.sh` files that way). If you get a `Permission denied` error when trying to run it, this is almost always the reason - just run the `chmod +x` command above.

## How do I know it worked?
The appearance of hdmcg varys from DCC to DCC:
- **Maya** shows `hdmcg` shelf tab.
- **Blender** shows a `hdmcg` menu.

## Set up PySide6 for Blender
In order to use some of the hdmcg-tools in Blender, a working verion of PySide6 is required. In case PySide6 is not setup (correctly) the pure Blender tools of hdmcg will still work. To set up PySide6 for Blender-use follow these steps:

- Make sure Python 3 is installed on your system.
- Create the venv in a folder where it doesn't bother you. In the example below a folder "venvs" is used.

   ```powershell
   cd C:\Users\<you>\Documents\venvs\
   python -m venv hdmcg
   ```
- The savest way to install PySide6 **into that venv** is to activate the venv and then use pip. To activate the venv be sure you are still in the vevns-folder and on Windows-Powershell type:
  ```powershell
  hdmcg/Scripts/Activate.ps1
  ```
  On Mac/Linux use:
  ```bash
  source hdmcg/bin/activate
  ```
- Then just use pip to install PySide:
   ```powershell
   pip install PySide6
   ```
- Set the BLENDER_PYSIDE environment variable in your Blender launcher *before* the line that starts Blender. It has to point too the `Lib\site-packages` folder inside **your** created venv:

   ```bat
   @echo off
   call hdmcg.bat

   set BLENDER_PYSIDE=C:\Users\<you>\Documents\venvs\hdmcg\Lib\site-packages
   set BLENDER="C:\Program Files\Blender Foundation\Blender 5.2\blender-launcher.exe"
   %BLENDER% --python %~dp0\hdmcg\blender\bootstrap.py
   ```

If you now start Blender via your launcher, the "I
need a cat" tool (amongst others) should show up in the `hdmcg` menu.

**If it still doesn't work:** open Blender's *Scripting* tab and check the
system console for a line starting with `[hdmcg] PySide6 nicht verfügbar`.
That means Blender still can't find/import PySide6 — double check the
`BLENDER_PYSIDE` path is spelled correctly and actually contains a
`PySide6` folder. Everything else in hdmcg keeps working fine even if this
step is skipped or broken; you just won't get the PySide6 based tools.

## Optional on Windows: Desktop shortcut with proper icon

Once your launcher `.bat` works from double-clicking it, you can make it a desktop shortcut: right-click the `.bat` file → *Send to* → *Desktop (create shortcut)* → rename it to whatever you like. Via right-click > Properties ("Eigenschaften") you also can assign an icon of your liking and attach the links to your task bar.
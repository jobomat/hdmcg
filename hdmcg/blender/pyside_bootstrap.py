import os
import site
import sys

import bpy

_pyside_ready = False


def init_pyside() -> bool:
    """
    Macht PySide6 fuer die hdmcg-Blender-Module verfuegbar. BLENDER_PYSIDE ist dabei nur ein
    optionales zusaetzliches site-dir (z.B. venv) - der Import wird auch ohne gesetzte env var
    versucht, falls PySide6 bereits anderweitig verfuegbar ist (z.B. durch Ayon o.Ae.). Schlaegt
    der Import fehl oder ist bereits eine andere Qt-Bindung geladen, wird das geloggt statt den
    Blender-Start zu crashen.
    """
    global _pyside_ready
    if _pyside_ready:
        return True

    other_bindings = [m for m in ("PySide2", "PyQt5", "PyQt6") if m in sys.modules]
    if other_bindings:
        print(f"[hdmcg] Warnung: {', '.join(other_bindings)} bereits im Prozess geladen "
              f"- gleichzeitiges Laden von PySide6 kann zu Qt-Konflikten fuehren.")

    pyside_sitepackages = os.environ.get("BLENDER_PYSIDE")
    if pyside_sitepackages:
        site.addsitedir(pyside_sitepackages)

    try:
        global QtWidgets, Qt
        from PySide6 import QtWidgets
        from PySide6.QtCore import Qt
    except ImportError as exc:
        hint = f" (BLENDER_PYSIDE={pyside_sitepackages})" if pyside_sitepackages else ""
        print(f"[hdmcg] PySide6 nicht verfuegbar{hint}: {exc}. PySide-Module werden nicht registriert.")
        return False

    bpy.app.timers.register(_pump_qt_events, first_interval=0.05)
    _pyside_ready = True
    return True


def get_qapp():
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])
        _pump_qt_events()  # einmaliger Sofort-Pump
    return app


def _pump_qt_events():
    app = QtWidgets.QApplication.instance()
    if app:
        app.processEvents()
    return 0.05  # alle 50ms erneut aufrufen (bpy.app.timers)

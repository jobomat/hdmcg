import importlib

import bpy

MENU_IDNAME = "TOPBAR_MT_hdmcg"

_menu_entries = []    # (bl_idname, label), in Lade-Reihenfolge
_loaded_modules = []  # erfolgreich geladene Modul-Objekte


class TOPBAR_MT_hdmcg(bpy.types.Menu):
    bl_label = "hdmcg"
    bl_idname = MENU_IDNAME

    def draw(self, context):
        layout = self.layout
        for bl_idname, label in _menu_entries:
            layout.operator(bl_idname, text=label)


def _draw_hdmcg_menu(self, context):
    self.layout.menu(MENU_IDNAME)


def setup(module_names: list[str], pyside_ok: bool) -> None:
    """
    Importiert und registriert jedes Modul aus module_names. Ein Modul folgt der Konvention
    register()/unregister(), optional MENU_ITEMS = [(bl_idname, label), ...] fuer Eintraege im
    HDMCG-Menue und optional REQUIRES_PYSIDE = True, um beim Fehlen von PySide uebersprungen
    zu werden (statt eines ImportErrors).
    """
    bpy.utils.register_class(TOPBAR_MT_hdmcg)
    bpy.types.TOPBAR_MT_editor_menus.append(_draw_hdmcg_menu)

    for name in module_names:
        module = importlib.import_module(name)

        if getattr(module, "REQUIRES_PYSIDE", False) and not pyside_ok:
            print(f"[hdmcg] {name} benoetigt PySide6 - wird uebersprungen (nicht verfuegbar).")
            continue

        module.register()
        _loaded_modules.append(module)
        _menu_entries.extend(getattr(module, "MENU_ITEMS", []))


def teardown() -> None:
    for module in reversed(_loaded_modules):
        module.unregister()
    _loaded_modules.clear()
    _menu_entries.clear()

    bpy.types.TOPBAR_MT_editor_menus.remove(_draw_hdmcg_menu)
    bpy.utils.unregister_class(TOPBAR_MT_hdmcg)

import bpy

from hdmcg.blender import pyside_bootstrap

REQUIRES_PYSIDE = True
MENU_ITEMS = [("hdmcg.devtools", "Open Dev Tools")]

_devtools_window = None


class LAUNCH_OT_hdmcg_devtools(bpy.types.Operator):
    bl_idname = "hdmcg.devtools"
    bl_label = "Open Dev Tools"
    bl_options = {'REGISTER'}

    def execute(self, context):
        global _devtools_window
        pyside_bootstrap.get_qapp()

        if _devtools_window is not None:
            try:
                _devtools_window.raise_()
                _devtools_window.activateWindow()
                return {'FINISHED'}
            except RuntimeError:
                # C++-Objekt wurde bereits zerstört (z.B. WA_DeleteOnClose griff)
                _devtools_window = None

        from hdmcg.shared.dev import DevTools
        _devtools_window = DevTools(module_filter="hdmcg", envvar_filter="OCIO")
        _devtools_window.setAttribute(pyside_bootstrap.Qt.WA_DeleteOnClose)

        def _on_destroyed():
            global _devtools_window
            _devtools_window = None
        _devtools_window.destroyed.connect(_on_destroyed)

        _devtools_window.show()
        return {'FINISHED'}


def register():
    bpy.utils.register_class(LAUNCH_OT_hdmcg_devtools)


def unregister():
    bpy.utils.unregister_class(LAUNCH_OT_hdmcg_devtools)

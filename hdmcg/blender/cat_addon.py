import bpy

from hdmcg.blender import pyside_bootstrap

REQUIRES_PYSIDE = True
MENU_ITEMS = [("hdmcg.cat", "I need a cat.")]

_cat_window = None


class LAUNCH_OT_hdmcg_cat(bpy.types.Operator):
    bl_idname = "hdmcg.cat"
    bl_label = "Open Dev Tools"
    bl_options = {'REGISTER'}

    def execute(self, context):
        global _cat_window
        pyside_bootstrap.get_qapp()

        if _cat_window is not None:
            try:
                _cat_window.raise_()
                _cat_window.activateWindow()
                return {'FINISHED'}
            except RuntimeError:
                # C++-Objekt wurde bereits zerstört (z.B. WA_DeleteOnClose griff)
                _cat_window = None

        from hdmcg.shared.cat import CatWidget
        _cat_window = CatWidget()
        _cat_window.setAttribute(pyside_bootstrap.Qt.WA_DeleteOnClose)

        def _on_destroyed():
            global _cat_window
            _cat_window = None
        _cat_window.destroyed.connect(_on_destroyed)

        _cat_window.show()
        return {'FINISHED'}


def register():
    bpy.utils.register_class(LAUNCH_OT_hdmcg_cat)


def unregister():
    bpy.utils.unregister_class(LAUNCH_OT_hdmcg_cat)

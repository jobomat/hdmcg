import bpy
from hdmcg.blender.utils import info

MENU_ITEMS = [("hdmcg.hello", "Hello")]


class HDMCG_OT_hello(bpy.types.Operator):
    bl_idname = "hdmcg.hello"
    bl_label = "Hello"

    def execute(self, context):
        self.report({'INFO'}, "Hello!")
        info("Hello!")
        return {'FINISHED'}


def register():
    bpy.utils.register_class(HDMCG_OT_hello)


def unregister():
    bpy.utils.unregister_class(HDMCG_OT_hello)
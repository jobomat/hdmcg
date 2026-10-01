from functools import partial
import os
import bpy


def info(msg: str) -> None:
    bpy.context.window_manager.popup_menu(
        lambda self, ctx: self.layout.label(text=str(msg)),
        title="Info", icon='INFO'
    )


def get_asset_paths():
    asset_library_pairs = os.environ.get("ASSET_LIBRARIES")
    return [p.split(",") for p in asset_library_pairs.split(";")] if asset_library_pairs else []


def mount_asset_library(lib_name, asset_path):
    """Injects a library into memory and binds pre/post save handlers."""
    if not asset_path or not os.path.exists(asset_path):
        return

    asset_libraries = bpy.context.preferences.filepaths.asset_libraries
    
    # 1. Mount into RAM if missing
    if lib_name not in asset_libraries:
        bpy.ops.preferences.asset_library_add(hide_props_region=False)
        new_lib = asset_libraries[-1]
        new_lib.name = lib_name
        new_lib.path = asset_path
        print(f"[Pipeline] Asset library mounted: {lib_name} -> {asset_path}")

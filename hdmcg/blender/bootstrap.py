import os, sys
from pathlib import Path

# hdmcg "self-appending"
_hdmcg_root = str(Path(__file__).resolve().parent.parent.parent)
if _hdmcg_root not in sys.path:
    sys.path.append(_hdmcg_root)

from hdmcg.blender import pyside_bootstrap, registry
from hdmcg.blender.utils import get_asset_paths, mount_asset_library

MODULES = [
    "hdmcg.blender.hello",
    "hdmcg.blender.devtools_addon",
    "hdmcg.blender.cat_addon",
]


def register():
    pyside_ok = pyside_bootstrap.init_pyside()
    registry.setup(MODULES, pyside_ok=pyside_ok)

    for lib_name, asset_path in get_asset_paths():
        mount_asset_library(lib_name, asset_path)


def unregister():
    registry.teardown()


register()

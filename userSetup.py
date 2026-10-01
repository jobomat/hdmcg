from maya.utils import executeDeferred
from maya import mel
from maya import cmds


def add_shelf_icon():
    _SHELF = mel.eval("$tmp = $gShelfTopLevel;")
    cmds.shelfTabLayout(_SHELF, edit=True, tabIcon=("hdmcg", "tiny_heart.png"))


def add_hotkeys():
    import hdmcg.maya.hotkeys


executeDeferred(add_shelf_icon)
executeDeferred(add_hotkeys)
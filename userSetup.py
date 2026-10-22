from maya.utils import executeDeferred
from maya import mel
from maya import cmds


def add_shelf_icon():
    _SHELF = mel.eval("$tmp = $gShelfTopLevel;")
    cmds.shelfTabLayout(_SHELF, edit=True, tabIcon=("hdmcg", "tiny_heart.png"))


def add_hotkeys():
    import hdmcg.maya.hotkeys


def add_toolbox_buttons():
    from hdmcg.maya.toolbox import add_toolbox_buttons
    add_toolbox_buttons()


executeDeferred(add_shelf_icon)
executeDeferred(add_hotkeys)
executeDeferred(add_toolbox_buttons)
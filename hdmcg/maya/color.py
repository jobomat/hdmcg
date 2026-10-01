import maya.cmds as cmds


def get_color(obj:str) -> (tuple | list | int):
    """Get wireframe color for nodes.
    Returnvalue is of type:
        - None:     if color override is off,
        - tuple:    if the color is set to RGB,
        - int:      if the color is set to index.
    """
    if not cmds.getAttr(f"{obj}.overrideEnabled"):
        return None
    
    if cmds.getAttr(f"{obj}.overrideRGBColors"):
        return cmds.getAttr(f"{obj}.overrideColorRGB")[0]
    else:
        return cmds.getAttr(f"{obj}.overrideColor")


def set_color(obj:str, color:(tuple | list | int)):
    """Set wireframe color for nodes of type mesh and Curves"""
    is_rgb = isinstance(color, (tuple, list))

    cmds.setAttr(f"{obj}.overrideEnabled", True)
    cmds.setAttr(f"{obj}.overrideRGBColors", is_rgb)

    if is_rgb:
        cmds.setAttr(f"{obj}.overrideColorRGB", *color, type="double3")
    else:
        cmds.setAttr(f"{obj}.overrideColor", color)


def set_wireframe_color(objs:list, color:(tuple | list), on_shapes=False):
    """Set wireframe color for obj."""
    if on_shapes:
        shapes = []
        for o in objs:
            shapes.extend(cmds.listRelatives(o, s=True, path=True))
        objs = shapes
    for o in objs:
        set_color(o, color)

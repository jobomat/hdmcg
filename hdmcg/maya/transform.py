import maya.cmds as cmds


def add_group(transform:str):
    """Add a group node above the given transform node.
    The group will be positioned and rotated to match the transform node,
    and the transform node will be parented under the group.
    The group will be parented under the same parent as the transform node, if it has one.
    """
    # Get the parent of the transform node, if it has one
    parent = cmds.listRelatives(transform, parent=True)
    if parent:
        parent = parent[0]

    # Create a new group node
    group = cmds.group(empty=True, name=transform.split("|")[-1] + '_grp')

    # Match the position and rotation of the transform node
    cmds.matchTransform(group, transform)

    # Parent the transform node under the group
    cmds.parent(transform, group)

    # Parent the group under the same parent as the transform node, if it has one
    if parent:
        cmds.parent(group, parent)

    return group


def set_lock_hide(obj:str, channels:list[bool, bool, bool, bool]):
    """Set lock/hide state of Translate, Rotate, Scale, Visibility channels of the given object."""
    # Define the channel names
    channel_names = ['translate', 'rotate', 'scale']

    # Loop through the channels and set the locked state
    for channel, lock in zip(channel_names, channels[:-1]):
        cmds.setAttr(f'{obj}.{channel}X', lock=lock, keyable=not lock)
        cmds.setAttr(f'{obj}.{channel}Y', lock=lock, keyable=not lock)
        cmds.setAttr(f'{obj}.{channel}Z', lock=lock, keyable=not lock)
    # Set the locked state of the visibility channel
    cmds.setAttr(f'{obj}.visibility', lock=channels[-1], keyable=not channels[-1])


def toggle_lock_hide(obj:str, channels:list[bool, bool, bool, bool]):
    """Toggle lock/hide state of Translate, Rotate, Scale, Visibility channels of the given object."""
    # Define the channel names
    channel_names = ['translate', 'rotate', 'scale']
    axes = ['X', 'Y', 'Z']

    # Loop through the channels and toggle the locked state
    for channel, lock in zip(channel_names, channels[:-1]):
        for axis in axes:
            current_lock = cmds.getAttr(f'{obj}.{channel}{axis}', lock=True)
            new_lock = not current_lock if lock else current_lock
            cmds.setAttr(f'{obj}.{channel}{axis}', lock=new_lock, keyable=not new_lock)
    # Toggle the locked state of the visibility channel
    current_visibility_lock = cmds.getAttr(f'{obj}.visibility', lock=True)
    new_visibility_lock = not current_visibility_lock if channels[-1] else current_visibility_lock
    cmds.setAttr(f'{obj}.visibility', lock=new_visibility_lock, keyable=not new_visibility_lock)


def set_unrenderable(mesh_transform:str):
    attrs = {
        "overrideEnabled": True,
        "overrideShading": False
    }
    for attr, val in attrs.items():
        cmds.setAttr(f"{mesh_transform}.{attr}", val)
    attrs = {
        "castsShadows": False,
        "receiveShadows": False,
        "motionBlur": False,
        "primaryVisibility": False,
        "smoothShading": False,
        "visibleInReflections": False,
        "visibleInRefractions": False,
        "doubleSided": False
    }
    for shape in cmds.listRelatives(mesh_transform, s=True, path=True):
        for attr, val in attrs.items():
            cmds.setAttr(f"{shape}.{attr}", val)


def set_renderable(mesh_transform:str):
    attrs = {
        "overrideEnabled": False,
        "overrideShading": True
    }
    for attr, val in attrs.items():
        cmds.setAttr(f"{mesh_transform}.{attr}", val)
    attrs = {
        "castsShadows": True,
        "receiveShadows": True,
        "motionBlur": True,
        "primaryVisibility": True,
        "smoothShading": True,
        "visibleInReflections": True,
        "visibleInRefractions": True,
        "doubleSided": True
    }
    for shape in cmds.listRelatives(mesh_transform, s=True, path=True):
        for attr, val in attrs.items():
            cmds.setAttr(f"{shape}.{attr}", val)


def toggle_renderable(mesh_transform:str):
    """Toggle renderable state of a mesh transform node."""
    is_visible = cmds.getAttr(f"{mesh_transform}.primaryVisibility")
    
    if is_visible:
        set_unrenderable(mesh_transform)
    else:
        set_renderable(mesh_transform)


def toggle_selectable(mesh_transform:str):
    """Toggle selectable state of a mesh transform node."""
    is_not_selectable = cmds.getAttr(f"{mesh_transform}.overrideDisplayType")

    print(is_not_selectable)
    
    if is_not_selectable:
        cmds.setAttr(f"{mesh_transform}.overrideDisplayType", 0)
    else:
        cmds.setAttr(f"{mesh_transform}.overrideDisplayType", 2)
        cmds.setAttr(f"{mesh_transform}.overrideEnabled", True)

import math
import maya.cmds as cmds
import maya.api.OpenMaya as om
from hdmcg.maya.color import get_color, set_color


def get_shapes(obj):
    """Returns all non-intermediate shape nodes of a transform."""
    if cmds.objectType(obj, isAType="shape"):
        return [obj]
    shapes = cmds.listRelatives(obj, shapes=True, noIntermediate=True, fullPath=True) or []
    if not shapes:
        raise ValueError(f"No shape found for: {obj}")
    return shapes


def get_world_points(obj):
    """
    Returns world-space coordinates of ALL points across ALL shapes of a transform
    (CVs for NURBS curves, vertices for poly meshes, arbitrarily mixed).
    """
    shapes = get_shapes(obj)
    all_points = []

    for shape in shapes:
        shape_type = cmds.objectType(shape)

        if shape_type == "nurbsCurve":
            comp = f"{shape}.cv[*]"
        elif shape_type == "mesh":
            comp = f"{shape}.vtx[*]"
        else:
            # skip other shape types (e.g. locators)
            continue

        cvs = cmds.ls(comp, flatten=True)
        points = [cmds.xform(cv, q=True, ws=True, t=True) for cv in cvs]
        all_points.extend(points)

    if not all_points:
        raise ValueError(f"No evaluable points found for: {obj}")

    return all_points


def rms_radius(points):
    """RMS distance of points from their common centroid."""
    n = len(points)
    cx = sum(p[0] for p in points) / n
    cy = sum(p[1] for p in points) / n
    cz = sum(p[2] for p in points) / n

    sq_sum = 0.0
    for p in points:
        dx, dy, dz = p[0] - cx, p[1] - cy, p[2] - cz
        sq_sum += dx*dx + dy*dy + dz*dz

    return math.sqrt(sq_sum / n)


def get_scale_factor(obj1, obj2):
    """
    Scale factor for obj2 so that its size (RMS radius) matches that of obj1.
    Supports multi-shape transforms (multiple curves/meshes per object),
    mixed NURBS/poly.
    """
    points1 = get_world_points(obj1)
    points2 = get_world_points(obj2)

    r1 = rms_radius(points1)
    r2 = rms_radius(points2)

    if r2 == 0:
        raise ValueError(f"{obj2}: RMS radius is 0, scaling not possible.")

    return r1 / r2


def add_shape(source_transform:str, target_transform:str, replace=True, with_color=False):
    """Adds or replaces the shape of the target transform with the shape of the source transform.
    The scale of the source transform is adjusted to match the scale of the target transform before adding the shape.
    If replace is True, the existing shapes of the target transform are deleted after adding the new shape.

    Args:
        source_transform (str): Long name of the source transform. (cmds.ls(sl=True, long=True))
        target_transform (str): Long name of the target transform. (cmds.ls(sl=True, long=True))
        replace (bool, optional): Defaults to True.
    """
    color = get_color(source_transform) if with_color else get_color(target_transform)
    source_transform = cmds.duplicate(source_transform)[0]
    if cmds.listRelatives(source_transform, allParents=True, path=True):
        source_transform = cmds.parent(source_transform, world=True)[0]
    
    source_shapes = cmds.listRelatives(source_transform, shapes=True, path=True)
    target_shapes = cmds.listRelatives(target_transform, shapes=True, path=True)
    
    s = get_scale_factor(target_transform, source_transform)
    
    cmds.setAttr(f'{source_transform}.scale', s, s, s, type="double3")
    cmds.setAttr(f'{source_transform}.rotate', 0, 0, 0, type="double3")
    cmds.setAttr(f'{source_transform}.translate', 0, 0, 0, type="double3")
    
    cmds.makeIdentity(source_transform, apply=True)
    
    cmds.parent(source_shapes[0], target_transform, shape=True, add=True)
    cmds.delete(source_transform)
    print("Deleting ", source_transform)
    
    if replace:
        cmds.delete(target_shapes)
    if with_color:
        set_color(target_transform, color)


def rotate_shapes(obj: str, axis: list[int], angle: float):
    """Rotates CVs/vertices of all shapes in obj by angle degrees around axis
    in object space. The transform node is not modified.

    Args:
        obj (str): Long name of the transform.
        axis (list[int]): Rotation axis as a 3-element vector, e.g. [1, 0, 0].
        angle (float): Rotation angle in degrees.
    """
    matrix = om.MQuaternion(math.radians(angle), om.MVector(*axis).normal()).asMatrix()

    for shape in get_shapes(obj):
        shape_type = cmds.objectType(shape)
        sel = om.MSelectionList()
        sel.add(shape)
        dag = sel.getDagPath(0)

        if shape_type == "nurbsCurve":
            fn = om.MFnNurbsCurve(dag)
            cvs = fn.cvPositions(om.MSpace.kObject)
            for i in range(len(cvs)):
                cvs[i] = cvs[i] * matrix
            fn.setCVPositions(cvs, om.MSpace.kObject)
            fn.updateCurve()
        elif shape_type == "mesh":
            fn = om.MFnMesh(dag)
            verts = fn.getPoints(om.MSpace.kObject)
            for i in range(len(verts)):
                verts[i] = verts[i] * matrix
            fn.setPoints(verts, om.MSpace.kObject)


def _dag_for_shape(shape: str):
    sel = om.MSelectionList()
    sel.add(shape)
    return sel.getDagPath(0)


def capture_shape_points(obj: str) -> dict:
    """Returns {shape_name: MPointArray} with current CV/vertex positions in object space."""
    result = {}
    for shape in get_shapes(obj):
        shape_type = cmds.objectType(shape)
        dag = _dag_for_shape(shape)
        if shape_type == "nurbsCurve":
            result[shape] = om.MFnNurbsCurve(dag).cvPositions(om.MSpace.kObject)
        elif shape_type == "mesh":
            result[shape] = om.MFnMesh(dag).getPoints(om.MSpace.kObject)
    return result


def apply_shape_points(captured: dict):
    """Writes back CV/vertex positions previously captured with capture_shape_points."""
    for shape, pts in captured.items():
        shape_type = cmds.objectType(shape)
        dag = _dag_for_shape(shape)
        if shape_type == "nurbsCurve":
            fn = om.MFnNurbsCurve(dag)
            fn.setCVPositions(pts, om.MSpace.kObject)
            fn.updateCurve()
        elif shape_type == "mesh":
            om.MFnMesh(dag).setPoints(pts, om.MSpace.kObject)


def scale_shapes_from_capture(captured: dict, factor: float):
    """Scales shapes by factor relative to captured baseline (around object-space origin = pivot)."""
    for shape, orig_pts in captured.items():
        shape_type = cmds.objectType(shape)
        dag = _dag_for_shape(shape)
        scaled = om.MPointArray(orig_pts)
        for i in range(len(scaled)):
            p = orig_pts[i]
            scaled[i] = om.MPoint(p.x * factor, p.y * factor, p.z * factor)
        if shape_type == "nurbsCurve":
            fn = om.MFnNurbsCurve(dag)
            fn.setCVPositions(scaled, om.MSpace.kObject)
            fn.updateCurve()
        elif shape_type == "mesh":
            om.MFnMesh(dag).setPoints(scaled, om.MSpace.kObject)

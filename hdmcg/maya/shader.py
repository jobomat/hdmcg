import maya.cmds as cmds
import maya.api.OpenMaya as om


def normalize_shader_assignments(transform):
    """Erzwingt explizite Per-Face-Assignment für alle SGs eines Meshes,
    damit AbcExport -writeFaceSets sie garantiert erfasst."""
    
    shape = cmds.listRelatives(transform, shapes=True, noIntermediate=True, path=True)[0]
    plugs = cmds.listConnections(shape, type="shadingEngine", plugs=True)
    
    # eingesteckte wireframecolors -> indiz für per face assignment: exit
    if [p for p in plugs if p.endswith(".memberWireframeColor")]:
        return
    
    sgs = list(set(cmds.listConnections(shape, type="shadingEngine")))
    num_faces = cmds.polyEvaluate(shape, face=True)
    faces = f"{shape}.f[0:{num_faces - 1}]"
    # erst ein face mit per face assignment, sonst funktioniert es nicht...
    cmds.sets(f"{shape}.f[0]", edit=True, forceElement="initialShadingGroup")
    cmds.sets(faces, edit=True, forceElement=sgs[0])


# # z.B. so als pre-run vor dem publishen:

# for obj in cmds.ls(sl=True):
#     normalize_shader_assignments(obj)


def bake_pref(shape, rest_frame=None, name="Pref", world=True):
    """Speichert die aktuellen Vertexpositionen als mtoa_varying_<name> am Shape.
    shape = cmds.listRelatives(cmds.ls(sl=True)[0], shapes=True)[0]
    bake_pref(shape, rest_frame=1)
    """
    if rest_frame is not None:
        cmds.currentTime(rest_frame)

    sel = om.MSelectionList()
    sel.add(shape)
    dag = sel.getDagPath(0)
    space = om.MSpace.kWorld if world else om.MSpace.kObject
    pts = om.MFnMesh(dag).getPoints(space)          # MPointArray, deformierter Zustand!

    attr = "mtoa_varying_" + name
    if not cmds.attributeQuery(attr, node=shape, exists=True):
        cmds.addAttr(shape, longName=attr, dataType="pointArray")

    data = om.MFnPointArrayData().create(pts)
    plug = om.MFnDependencyNode(dag.node()).findPlug(attr, False)
    plug.setMObject(data)
    print("{}: {} Punkte nach .{} geschrieben".format(shape, len(pts), attr))

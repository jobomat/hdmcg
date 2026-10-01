import maya.cmds as cmds


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
